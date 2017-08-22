import React from 'react';
import { Button } from 'antd-mobile';
import { connect } from 'dva';
import styles from './IndexPage.css';
import Footer from '../components/MainLayout/Footer.jsx';


function IndexPage() {
  return (
    <div >
      <Footer />
    </div>
  );
}

IndexPage.propTypes = {
};

export default connect()(IndexPage);
