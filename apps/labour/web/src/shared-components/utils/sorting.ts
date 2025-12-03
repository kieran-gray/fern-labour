import { ContractionDTO, LabourDTO } from '@clients/labour_service';

export const sortContractions = (contractions: ContractionDTO[]): ContractionDTO[] => {
  return contractions.sort((a, b) =>
    a.start_time < b.start_time ? -1 : a.start_time > b.start_time ? 1 : 0
  );
};

export const sortLabours = (labours: LabourDTO[]): LabourDTO[] => {
  return labours.sort((a, b) => (a.due_date < b.due_date ? -1 : a.due_date > b.due_date ? 1 : 0));
};
