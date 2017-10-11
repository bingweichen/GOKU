// 购物页面首页
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'dva';
import { Flex } from 'antd-mobile';
import Profile from '../../components/Card/Profile';
import Header from '../../components/MainLayout/Header.jsx';
import styles from './index.less';

const { Item } = Flex;
function IndexContent({ cars, carType, changeCarType }) {
  return (
    <div className={styles.IndexContent}>
      <Header carType={carType} changeCarType={changeCarType} />
      <Flex style={{ flexWrap: 'wrap' }}>
        {
          cars.map(car => (
            <Item
              className={styles.item}
              key={car.name}
            >
              <Profile
                car={car}
              />
            </Item>
          ))
        }
      </Flex>
    </div>
  );
}

IndexContent.prototype = {
  cars: PropTypes.array,
};

const mapStateToProps = (state) => {
  const { cars, carType } = state.IndexPage;
  return {
    cars,
    carType,
  };
};

const dispatchToProps = (dispatch) => {
  return {
    changeCarType: (carType) => {
      dispatch({ type: 'IndexPage/changeCarType', carType });
    },
  };
};

export default connect(mapStateToProps, dispatchToProps)(IndexContent);
