import request from '../utils/request';

export function order({ page, number, days }) {
  return request.get(`manager/appointment_setting/appointments/all?page=${page}&&paginate_by=${number}` +
    `&&days=${days}`);
}

export function returnBike(bikeData) {
  return request({
    url: 'manager/appointment_setting/appointment/return_e_bike',
    method: 'POST',
    data: bikeData,
  });
}
