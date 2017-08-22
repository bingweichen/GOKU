import React from 'react';
import { connect } from 'dva';
import styles from './PickUpSite.less';

function PickUpSite({ allSite, adviceSite }) {
  return (
    <div>
      {
        allSite.map(site => (
          <div className={styles.item} key={site.name}>
            <p className={styles.shortName}>{site.name}
              <span style={{ color: 'green' }}>
                {adviceSite.name === site.name ? '(建议自提点)' : ''}
              </span>
            </p>
            <p className={styles.phone}>027-09876789</p>
            <p className={styles.address}>{site.address}</p>
          </div>
        ))
      }
    </div>
  );
}

const mapStateToProps = ({ order }) => {
  return {
    adviceSite: order.pickUpSite.adviceSite,
    allSite: order.pickUpSite.allSite,
  };
};

export default connect(mapStateToProps)(PickUpSite);
