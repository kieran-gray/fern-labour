import { LabourDTO } from '@clients/labour_service';
import { generateEventId } from '../utils/eventId';
import { db, GuestProfile } from './database';

/**
 * Guest profile management for anonymous local-only usage
 * Provides permanent storage until user upgrades to authenticated account
 */
export class GuestProfileManager {
  /**
   * Create a new guest profile
   */
  static async createGuestProfile(): Promise<GuestProfile> {
    const guestProfile: GuestProfile = {
      guestId: generateEventId(),
      createdAt: new Date(),
      labours: [],
      isUpgraded: 0,
      lastActiveAt: new Date(),
    };

    await db.guestProfiles.add(guestProfile);
    return guestProfile;
  }

  /**
   * Get current guest profile or create new one
   */
  static async getCurrentGuestProfile(): Promise<GuestProfile> {
    const profiles = await db.guestProfiles.where('isUpgraded').equals(0).toArray();
    if (profiles.length > 0) {
      const profile = profiles.sort(
        (a, b) => b.lastActiveAt.getTime() - a.lastActiveAt.getTime()
      )[0];
      await this.updateLastActive(profile.guestId);
      return (await db.guestProfiles.get(profile.guestId)) || profile;
    }
    return await this.createGuestProfile();
  }

  /**
   * Update guest profile's labour data
   */
  static async updateGuestLabours(guestId: string, labours: LabourDTO[]): Promise<void> {
    await db.guestProfiles.update(guestId, {
      labours,
      lastActiveAt: new Date(),
    });
  }

  /**
   * Add labour to guest profile
   */
  static async addGuestLabour(guestId: string, labour: LabourDTO): Promise<void> {
    const profile = await db.guestProfiles.get(guestId);
    if (!profile) {
      throw new Error(`Guest profile not found: ${guestId}`);
    }

    const updatedLabours = [...profile.labours, labour];
    await this.updateGuestLabours(guestId, updatedLabours);
  }

  /**
   * Update specific labour in guest profile
   */
  static async updateGuestLabour(
    guestId: string,
    labourId: string,
    updates: Partial<LabourDTO>
  ): Promise<void> {
    const profile = await db.guestProfiles.get(guestId);
    if (!profile) {
      throw new Error(`Guest profile not found: ${guestId}`);
    }

    const updatedLabours = profile.labours.map((labour) =>
      labour.id === labourId ? { ...labour, ...updates } : labour
    );

    await this.updateGuestLabours(guestId, updatedLabours);
  }

  /**
   * Delete labour from guest profile
   */
  static async deleteGuestLabour(guestId: string, labourId: string): Promise<void> {
    const profile = await db.guestProfiles.get(guestId);
    if (!profile) {
      throw new Error(`Guest profile not found: ${guestId}`);
    }

    const updatedLabours = profile.labours.filter((labour) => labour.id !== labourId);
    await this.updateGuestLabours(guestId, updatedLabours);
  }

  /**
   * Get all labours for guest profile
   */
  static async getGuestLabours(guestId: string): Promise<LabourDTO[]> {
    const profile = await db.guestProfiles.get(guestId);
    return profile?.labours || [];
  }

  /**
   * Get specific labour from guest profile
   */
  static async getGuestLabour(guestId: string, labourId: string): Promise<LabourDTO | undefined> {
    const labours = await this.getGuestLabours(guestId);
    return labours.find((labour) => labour.id === labourId);
  }

  /**
   * Update last active timestamp
   */
  static async updateLastActive(guestId: string): Promise<void> {
    await db.guestProfiles.update(guestId, { lastActiveAt: new Date() });
  }

  /**
   * Mark guest profile as upgraded and archive
   */
  static async markAsUpgraded(guestId: string): Promise<void> {
    await db.guestProfiles.update(guestId, {
      isUpgraded: 1,
      lastActiveAt: new Date(),
    });
  }

  /**
   * Export guest data for user download/backup
   */
  static async exportGuestData(guestId: string) {
    const profile = await db.guestProfiles.get(guestId);
    if (!profile) {
      throw new Error(`Guest profile not found: ${guestId}`);
    }

    return {
      exportedAt: new Date().toISOString(),
      guestId: profile.guestId,
      createdAt: (() => {
        try {
          return profile.createdAt instanceof Date
            ? profile.createdAt.toISOString()
            : new Date(profile.createdAt).toISOString();
        } catch {
          return new Date().toISOString();
        }
      })(),
      labours: profile.labours,
    };
  }

  /**
   * Clear guest profile data (user requested deletion)
   */
  static async clearGuestData(guestId: string): Promise<void> {
    await db.guestProfiles.delete(guestId);
  }

  /**
   * Get all guest profiles (for admin/debugging)
   */
  static async getAllGuestProfiles(): Promise<GuestProfile[]> {
    return await db.guestProfiles.toArray();
  }

  /**
   * Clean up old inactive guest profiles
   * Only called manually via user action - no automatic expiration
   */
  static async cleanupInactiveProfiles(daysInactive: number = 365): Promise<number> {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysInactive);

    const inactiveProfiles = await db.guestProfiles
      .where('lastActiveAt')
      .below(cutoffDate)
      .and((profile) => profile.isUpgraded === 0)
      .toArray();

    const profileIds = inactiveProfiles.map((p) => p.guestId);
    await db.guestProfiles.bulkDelete(profileIds);
    return profileIds.length;
  }
}
