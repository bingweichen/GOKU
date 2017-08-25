import request from '../utils/request';

export function order({ page, number }) {
  return request.get(`manager/appointment_setting/appointments/all?page=${page}&&paginate_by=${number}`);
}
