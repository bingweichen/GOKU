import React from 'react';
import { connect } from 'dva';
import styles from './IndexPage.css';
import Footer from '../components/MainLayout/Footer.jsx';


function IndexPage({ location }) {
  const tab = location.query.tab ? location.query.tab : 'shop';
  return (
    <div >
      <Footer tab={tab} />
    </div>
  );
}

IndexPage.propTypes = {
};

export default connect()(IndexPage);
