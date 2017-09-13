import axios from '../utils/axios';
import request from '../utils/request';

export function getPickUpSite(id) {
  const url = id ? `store/all?username=${id}` : 'store/all';
  return request(url);
}

export function buyCarOrder(submitData, id) {
  return axios({
    method: 'PUT',
    url: 'appointment',
    data: {
      username: id,
      ...submitData,
    },
  });
}

export function pickUpWithCarNumber({
  appointment_id,
  serial_number,
}) {
  return axios({
    method: 'POST',
    url: 'appointment/check/upload_serials_number',
    data: {
      appointment_id,
      serial_number,
    },
  });
}

export function paySuccess(id) {
  return axios({
    method: 'POST',
    url: 'appointment/status/total_payment_success',
    data: {
      appointment_id: id,
      openid: localStorage.getItem('openid'),
    },
  });
}

export function getOrder(appointmentId) {
  return axios.get(`appointment?appointment_id=${appointmentId}`);
}

export function repariCar(reason) {
  return axios({
    method: 'PUT',
    url: 'report_table',
    data: reason,
  });
}
