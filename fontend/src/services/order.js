import axios from 'axios';
import request from '../utils/request';

export function getPickUpSite(id) {
  const url = id ? `/api/store/all?username=${id}` : '/api/store/all';
  return request(url);
}

export function buyCarOrder({
  username, e_bike_model, color, category, type, note, coupon,
}) {
  return axios({
    method: 'PUT',
    url: '/api/appointment',
    data: {
      username,
      e_bike_model,
      color,
      category,
      type,
      note,
      coupon,
    },
  });
}

export function pickUpWithCarNumber({
  username,
  appointment_id,
  serial_number,
}) {
  return axios({
    method: 'POST',
    url: '/api/appointment/check/upload_serials_number',
    data: {
      username,
      appointment_id,
      serial_number,
    },
  });
}

export function paySuccess({
  username,
  appointment_id,
}) {
  return axios({
    method: 'POST',
    url: '/api/appointment/status/total_payment_success',
    data: {
      username,
      appointment_id,
    },
  });
}

export function getOrder(username, appointmentId) {
  return axios.get(`/api/appointment?username=${username}&&appointment_id=${appointmentId}`);
}
