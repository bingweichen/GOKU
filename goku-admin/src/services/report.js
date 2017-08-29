import request from '../utils/request';

export function getAllReport() {
  return request('manager/support/report_table/all');
}
