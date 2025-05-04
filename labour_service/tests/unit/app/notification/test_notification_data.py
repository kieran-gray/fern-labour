from src.notification.notification_data import (
    ContactUsData,
    LabourAnnouncementData,
    LabourBegunData,
    LabourCompletedData,
    LabourCompletedWithNoteData,
    LabourInviteData,
    LabourUpdateData,
    SubscriberApprovedData,
    SubscriberInviteData,
    SubscriberRequestedData,
)


def test_can_serialize_and_deserialize_labour_update_data():
    data_dict = {
        "birthing_person_name": "name",
        "subscriber_first_name": "lastName",
        "update": "Message",
        "link": "http://test.com",
        "notes": "No notes",
    }
    labour_update_data = LabourUpdateData.from_dict(data=data_dict)
    assert isinstance(labour_update_data, LabourUpdateData)
    assert data_dict == labour_update_data.to_dict()


def test_can_serialize_and_deserialize_labour_announcement_data():
    data_dict = {
        "birthing_person_name": "firstName lastName",
        "birthing_person_first_name": "firstName",
        "subscriber_first_name": "lastName",
        "announcement": "Message",
        "link": "http://test.com",
    }
    labour_announcement_data = LabourAnnouncementData.from_dict(data=data_dict)
    assert isinstance(labour_announcement_data, LabourAnnouncementData)
    assert data_dict == labour_announcement_data.to_dict()


def test_can_serialize_and_deserialize_labour_begun_data():
    data_dict = {
        "birthing_person_name": "firstName lastName",
        "birthing_person_first_name": "firstName",
        "subscriber_first_name": "lastName",
        "link": "http://test.com",
    }
    labour_begun_data = LabourBegunData.from_dict(data=data_dict)
    assert isinstance(labour_begun_data, LabourBegunData)
    assert data_dict == labour_begun_data.to_dict()


def test_can_serialize_and_deserialize_labour_completed_data():
    data_dict = {
        "birthing_person_name": "firstName lastName",
        "birthing_person_first_name": "firstName",
        "subscriber_first_name": "lastName",
        "link": "http://test.com",
    }
    labour_completed_data = LabourCompletedData.from_dict(data=data_dict)
    assert isinstance(labour_completed_data, LabourCompletedData)
    assert data_dict == labour_completed_data.to_dict()


def test_can_serialize_and_deserialize_labour_completed_with_note_data():
    data_dict = {
        "birthing_person_name": "firstName lastName",
        "birthing_person_first_name": "firstName",
        "subscriber_first_name": "lastName",
        "update": "Message",
        "link": "http://test.com",
    }
    labour_completed_with_note_data = LabourCompletedWithNoteData.from_dict(data=data_dict)
    assert isinstance(labour_completed_with_note_data, LabourCompletedWithNoteData)
    assert data_dict == labour_completed_with_note_data.to_dict()


def test_can_serialize_and_deserialize_contact_us_data():
    data_dict = {
        "email": "test@email.com",
        "name": "test",
        "message": "test message",
        "user_id": "test_user_id",
    }
    contact_us_data = ContactUsData.from_dict(data=data_dict)
    assert isinstance(contact_us_data, ContactUsData)
    assert data_dict == contact_us_data.to_dict()


def test_can_serialize_and_deserialize_labour_invite_data():
    data_dict = {
        "birthing_person_name": "test name",
        "birthing_person_first_name": "test",
        "link": "http://test.com",
    }
    labour_invite_data = LabourInviteData.from_dict(data=data_dict)
    assert isinstance(labour_invite_data, LabourInviteData)
    assert data_dict == labour_invite_data.to_dict()


def test_can_serialize_and_deserialize_subscriber_invite_data():
    data_dict = {
        "subscriber_name": "test name",
        "link": "http://test.com",
    }
    subscriber_invite_data = SubscriberInviteData.from_dict(data=data_dict)
    assert isinstance(subscriber_invite_data, SubscriberInviteData)
    assert data_dict == subscriber_invite_data.to_dict()


def test_can_serialize_and_deserialize_subscriber_requested_data():
    data_dict = {
        "birthing_person_first_name": "user",
        "subscriber_name": "test name",
        "link": "http://test.com",
    }
    subscriber_invite_data = SubscriberRequestedData.from_dict(data=data_dict)
    assert isinstance(subscriber_invite_data, SubscriberRequestedData)
    assert data_dict == subscriber_invite_data.to_dict()


def test_can_serialize_and_deserialize_subscriber_approved_data():
    data_dict = {
        "birthing_person_name": "user name",
        "subscriber_first_name": "test",
        "link": "http://test.com",
    }
    subscriber_invite_data = SubscriberApprovedData.from_dict(data=data_dict)
    assert isinstance(subscriber_invite_data, SubscriberApprovedData)
    assert data_dict == subscriber_invite_data.to_dict()
