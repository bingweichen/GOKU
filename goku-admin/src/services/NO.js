import request from '../utils/request';

export function getAllSerialNumber({ page, pageSize }) {
  return request.get(`manager/basic_setting/serial_number/all?page=${page}&&paginate_by=${pageSize}`);
}
