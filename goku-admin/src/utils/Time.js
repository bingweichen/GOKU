import moment from 'moment';

export function formatDate(time) {
  return moment(time).format('YYYY年MM月DD日 HH:mm');
}
