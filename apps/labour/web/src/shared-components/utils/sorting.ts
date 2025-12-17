import { ContractionReadModel, LabourReadModel } from '@base/clients/labour_service_v2';

export const sortContractions = (contractions: ContractionReadModel[]): ContractionReadModel[] => {
  return contractions.sort((a, b) =>
    a.duration.start_time < b.duration.start_time
      ? -1
      : a.duration.start_time > b.duration.start_time
        ? 1
        : 0
  );
};

export const sortLabours = (labours: LabourReadModel[]): LabourReadModel[] => {
  return labours.sort((a, b) => (a.due_date < b.due_date ? -1 : a.due_date > b.due_date ? 1 : 0));
};
