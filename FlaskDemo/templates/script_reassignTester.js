import React from 'react';

import Select from 'react-select';
import { locationOptions } from './data';

export default () => (
  <Select
    defaultValue={[locationOptions[0], locationOptions[1]]}
    isMulti
    name="colors"
    options={locationOptions}
    className="basic-multi-select"
    classNamePrefix="select"
    style= {{width: '82%'}} 
    //autosize = {false}
  />
);