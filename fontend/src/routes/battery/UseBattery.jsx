import React, { Component } from 'react';
import { Modal } from 'antd-mobile';
import { rentBattery } from '../../services/battery.js';
import Button from '../../components/Button';
import styles from './index.less';

class UseBattery extends Component {

  state = {
    errorModal: false,
  }

  async useBattery(number) {
    try {
      await rentBattery(number);
    } catch (error) {
      this.setState({ errorModal: true });
    }
  }

  render() {
    const { number } = this.props.location.query;
    return (
      <div className={styles.usebattery}>
        <div className={styles.batterInfo}>
          <p><span>闪充编号</span></p>
          <p>{number}</p>
        </div>
        <div className={styles.useMessage}>
          <Button
            style={{ width: '100%' }}
            onClick={() => { this.useBattery(number); }}
          >确认使用</Button>
          {/* <p>未交押金，无法享受闪充服务
          <span style={{ color: '#FF5B55' }}> 去充值</span>
          </p> */}
        </div>
        <Modal
          title="使用闪充失败"
          transparent
          maskClosable={false}
          visible={this.state.errorModal}
          footer={[{ text: '确定', onPress: () => { this.setState({ errorModal: false }); } }]}
        >
          你现在暂时不能使用闪充
        </Modal>
      </div>
    );
  }
}

export default UseBattery;
