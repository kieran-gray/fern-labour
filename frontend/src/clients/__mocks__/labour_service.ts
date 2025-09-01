export const ContractionsService = {
  startContraction: jest.fn(),
  endContraction: jest.fn(),
  updateContraction: jest.fn(),
  deleteContraction: jest.fn(),
};

export const LabourService = {
  planLabour: jest.fn(),
  completeLabour: jest.fn(),
  deleteLabour: jest.fn(),
  updateLabourPlan: jest.fn(),
  sendInvite: jest.fn(),
};

export const LabourUpdatesService = {
  createLabourUpdate: jest.fn(),
};

export const LabourQueriesService = {
  getActiveLabour: jest.fn(),
  getLabourById: jest.fn(),
  getAllLabours: jest.fn(),
};
