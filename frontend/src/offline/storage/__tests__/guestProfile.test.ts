import 'fake-indexeddb/auto';

import { LabourDTO } from '@clients/labour_service';
import { OfflineDatabase } from '../database';
import { GuestProfileManager } from '../guestProfile';

describe('GuestProfileManager', () => {
  let testDb: OfflineDatabase;

  beforeEach(async () => {
    testDb = new OfflineDatabase();
    await testDb.open();
    await testDb.transaction(
      'rw',
      [testDb.outbox, testDb.guestProfiles, testDb.sequences],
      async () => {
        await testDb.outbox.clear();
        await testDb.guestProfiles.clear();
        await testDb.sequences.clear();
      }
    );
  });

  afterEach(async () => {
    if (testDb.isOpen()) {
      await testDb.close();
    }
  });

  const createMockLabour = (overrides: Partial<LabourDTO> = {}): LabourDTO => ({
    id: `labour-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    birthing_person_id: 'guest-123',
    current_phase: 'active',
    due_date: '2023-06-01',
    first_labour: true,
    labour_name: 'Test Labour',
    start_time: '2023-05-15T10:00:00Z',
    end_time: null,
    notes: null,
    recommendations: {},
    contractions: [],
    labour_updates: [],
    ...overrides,
  });

  describe('profile lifecycle', () => {
    it('should create and retrieve guest profiles', async () => {
      const profile1 = await GuestProfileManager.createGuestProfile();
      const profile2 = await GuestProfileManager.createGuestProfile();

      expect(profile1.guestId).toBeDefined();
      expect(profile2.guestId).toBeDefined();
      expect(profile1.guestId).not.toBe(profile2.guestId);

      expect(profile1.labours).toEqual([]);
      expect(profile1.isUpgraded).toBe(0);
      expect(profile1.createdAt).toBeInstanceOf(Date);
      expect(profile1.lastActiveAt).toBeInstanceOf(Date);
    });

    it('should get current profile or create new one', async () => {
      // First call should create a profile
      const profile1 = await GuestProfileManager.getCurrentGuestProfile();
      expect(profile1.guestId).toBeDefined();

      // Second call should return the same profile (testing retrieval logic)
      const profile2 = await GuestProfileManager.getCurrentGuestProfile();
      expect(profile1.guestId).toBe(profile2.guestId);
    });

    it('should return most recent active profile', async () => {
      const profile1 = await GuestProfileManager.createGuestProfile();
      await GuestProfileManager.createGuestProfile();

      // Wait and update profile1 to have a much more recent lastActiveAt
      await new Promise((resolve) => setTimeout(resolve, 50));
      const futureTime = new Date(Date.now() + 1000 * 60); // 1 minute in the future
      await testDb.guestProfiles.update(profile1.guestId, {
        lastActiveAt: futureTime,
      });

      const currentProfile = await GuestProfileManager.getCurrentGuestProfile();
      expect(currentProfile.guestId).toBe(profile1.guestId); // Most recently active
    });

    it('should skip upgraded profiles when getting current', async () => {
      const profile = await GuestProfileManager.createGuestProfile();
      await GuestProfileManager.markAsUpgraded(profile.guestId);

      const currentProfile = await GuestProfileManager.getCurrentGuestProfile();
      expect(currentProfile.guestId).not.toBe(profile.guestId); // Should create new one
    });
  });

  describe('labour management', () => {
    let profile: Awaited<ReturnType<typeof GuestProfileManager.createGuestProfile>>;
    let mockLabour: LabourDTO;

    beforeEach(async () => {
      profile = await GuestProfileManager.createGuestProfile();
      mockLabour = createMockLabour();
    });

    it('should add labour to profile', async () => {
      await GuestProfileManager.addGuestLabour(profile.guestId, mockLabour);

      const labours = await GuestProfileManager.getGuestLabours(profile.guestId);
      expect(labours).toHaveLength(1);
      expect(labours[0]).toEqual(mockLabour);
    });

    it('should update specific labour', async () => {
      await GuestProfileManager.addGuestLabour(profile.guestId, mockLabour);

      const updates = {
        current_phase: 'completed' as const,
        end_time: '2023-05-15T18:00:00Z',
        notes: 'Labour completed successfully',
      };

      await GuestProfileManager.updateGuestLabour(profile.guestId, mockLabour.id, updates);

      const updatedLabour = await GuestProfileManager.getGuestLabour(
        profile.guestId,
        mockLabour.id
      );
      expect(updatedLabour?.current_phase).toBe('completed');
      expect(updatedLabour?.end_time).toBe('2023-05-15T18:00:00Z');
      expect(updatedLabour?.notes).toBe('Labour completed successfully');
      expect(updatedLabour?.id).toBe(mockLabour.id); // Other fields preserved
    });

    it('should delete specific labour', async () => {
      const labour2 = createMockLabour({ labour_name: 'Second Labour' });

      await GuestProfileManager.addGuestLabour(profile.guestId, mockLabour);
      await GuestProfileManager.addGuestLabour(profile.guestId, labour2);

      await GuestProfileManager.deleteGuestLabour(profile.guestId, mockLabour.id);

      const remainingLabours = await GuestProfileManager.getGuestLabours(profile.guestId);
      expect(remainingLabours).toHaveLength(1);
      expect(remainingLabours[0].id).toBe(labour2.id);
    });

    it('should handle operations on non-existent profile', async () => {
      await expect(GuestProfileManager.addGuestLabour('non-existent', mockLabour)).rejects.toThrow(
        'Guest profile not found'
      );

      await expect(
        GuestProfileManager.updateGuestLabour('non-existent', 'labour-id', {})
      ).rejects.toThrow('Guest profile not found');

      await expect(
        GuestProfileManager.deleteGuestLabour('non-existent', 'labour-id')
      ).rejects.toThrow('Guest profile not found');

      const labours = await GuestProfileManager.getGuestLabours('non-existent');
      expect(labours).toEqual([]);

      const labour = await GuestProfileManager.getGuestLabour('non-existent', 'labour-id');
      expect(labour).toBeUndefined();
    });

    it('should handle updates to non-existent labour gracefully', async () => {
      await GuestProfileManager.updateGuestLabour(profile.guestId, 'non-existent-labour', {
        current_phase: 'completed' as const,
      });

      const labours = await GuestProfileManager.getGuestLabours(profile.guestId);
      expect(labours).toHaveLength(0);
    });
  });

  describe('profile state management', () => {
    it('should update lastActiveAt during operations', async () => {
      const profile = await GuestProfileManager.createGuestProfile();
      const originalTime = profile.lastActiveAt.getTime();

      await new Promise((resolve) => setTimeout(resolve, 50));

      await GuestProfileManager.getCurrentGuestProfile();

      const updatedProfile = await testDb.guestProfiles.get(profile.guestId);
      expect(updatedProfile?.lastActiveAt.getTime()).toBeGreaterThan(originalTime);
    });

    it('should mark profile as upgraded', async () => {
      const profile = await GuestProfileManager.createGuestProfile();
      const originalTime = profile.lastActiveAt.getTime();

      await new Promise((resolve) => setTimeout(resolve, 10));

      await GuestProfileManager.markAsUpgraded(profile.guestId);

      const upgradedProfile = await testDb.guestProfiles.get(profile.guestId);
      expect(upgradedProfile?.isUpgraded).toBe(1);
      expect(upgradedProfile?.lastActiveAt.getTime()).toBeGreaterThan(originalTime);
    });

    it('should export complete guest data', async () => {
      const profile = await GuestProfileManager.createGuestProfile();
      const mockLabour = createMockLabour();

      await GuestProfileManager.addGuestLabour(profile.guestId, mockLabour);

      const exportData = await GuestProfileManager.exportGuestData(profile.guestId);

      expect(exportData.exportedAt).toBeDefined();
      expect(exportData.guestId).toBe(profile.guestId);
      expect(exportData.createdAt).toBeDefined();
      expect(exportData.labours).toEqual([mockLabour]);
    });

    it('should clear guest data', async () => {
      const profile = await GuestProfileManager.createGuestProfile();

      await GuestProfileManager.clearGuestData(profile.guestId);

      const deletedProfile = await testDb.guestProfiles.get(profile.guestId);
      expect(deletedProfile).toBeUndefined();
    });

    it('should handle export/clear on non-existent profile', async () => {
      await expect(GuestProfileManager.exportGuestData('non-existent')).rejects.toThrow(
        'Guest profile not found'
      );

      // clearGuestData should not throw for non-existent profile
      await expect(GuestProfileManager.clearGuestData('non-existent')).resolves.not.toThrow();
    });
  });

  describe('maintenance operations', () => {
    it('should cleanup inactive profiles while preserving active and upgraded ones', async () => {
      const now = Date.now();
      const oldDate = new Date(now - 400 * 24 * 60 * 60 * 1000); // 400 days ago
      const recentDate = new Date(now - 100 * 24 * 60 * 60 * 1000); // 100 days ago

      // Create profiles with different states
      const oldInactiveProfile = await GuestProfileManager.createGuestProfile();
      const oldUpgradedProfile = await GuestProfileManager.createGuestProfile();
      const recentProfile = await GuestProfileManager.createGuestProfile();

      // Set up test conditions
      await testDb.guestProfiles.update(oldInactiveProfile.guestId, {
        lastActiveAt: oldDate,
        isUpgraded: 0,
      });

      await testDb.guestProfiles.update(oldUpgradedProfile.guestId, {
        lastActiveAt: oldDate,
        isUpgraded: 1, // This one is upgraded
      });

      await testDb.guestProfiles.update(recentProfile.guestId, {
        lastActiveAt: recentDate,
        isUpgraded: 0,
      });

      const cleanedCount = await GuestProfileManager.cleanupInactiveProfiles(365);

      expect(cleanedCount).toBe(1); // Only old inactive should be removed

      // Verify correct profiles were removed/preserved
      expect(await testDb.guestProfiles.get(oldInactiveProfile.guestId)).toBeUndefined();
      expect(await testDb.guestProfiles.get(oldUpgradedProfile.guestId)).toBeDefined(); // Upgraded preserved
      expect(await testDb.guestProfiles.get(recentProfile.guestId)).toBeDefined(); // Recent preserved
    });

    it('should get all guest profiles for admin/debugging', async () => {
      await GuestProfileManager.createGuestProfile();
      await GuestProfileManager.createGuestProfile();

      const allProfiles = await GuestProfileManager.getAllGuestProfiles();
      expect(allProfiles).toHaveLength(2);
    });
  });
});
