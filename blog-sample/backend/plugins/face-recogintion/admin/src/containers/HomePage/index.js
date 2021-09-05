/*
 *
 * HomePage
 *
 */

import { Button } from '@buffetjs/core';
import { Header, Inputs } from '@buffetjs/custom';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import React, { memo, useState } from 'react';
import { useGlobalContext, useStrapi } from 'strapi-helper-plugin';
import Block from '../../components/Block';
import InputMedia from '../../components/InputMedia';
import getTrad from '../../utils/getTrad';
import { ContainerFluid, StyledRow } from './components';
import { addNewFace } from '../../utils/addFace';

const form = {
  name: {
    styleName: 'col-6',
    label: 'containers.HomePage.person.name',
    placeholder: 'containers.HomePage.enter.name',
    type: 'text',
    validations: {
      required: true
    },
  },
  file: {
    styleName: "col-6",
    label: 'containers.HomePage.person.face',
    placeholder: 'pick a file',
    type: 'media',
    validations: {
      required: true
    },
    multiple: false,
    value: ''
  }
}

const HomePage = () => {
  const globalContext = useGlobalContext();
  const { formatMessage } = globalContext;

  const [state, setState] = useState({});

  const handleChange = ({ target: { name, value } }) => {
    setState(prevState => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // console.log(state);
    if (state.file && state.name) {
      addNewFace(state);
      strapi.notification.success("face added successfully");
      setState({})
      e.target.reset();
    } else {
      strapi.notification.error("please fill all fields");
    }

  }


  return (
    <ContainerFluid className="container-fluid">
      <Header
        title={{
          label: formatMessage({
            id: getTrad('containers.HomePage.PluginHeader.title'),
          }),
        }}
        content={formatMessage({
          id: getTrad('containers.HomePage.PluginHeader.description'),
        })}
      />
      <Block>
        <form onSubmit={handleSubmit} >
          <StyledRow className="row">
            {Object.keys(form).map(input => {
              return (
                <div className={form[input].styleName} key={input}>
                  <Inputs
                    customInputs={{ media: InputMedia }}
                    onChange={handleChange}
                    name={input}
                    {...form[input]}
                    label={formatMessage({ id: getTrad(form[input].label) })}
                    placeholder={formatMessage({ id: getTrad(form[input].placeholder) })}
                    attribute={form[input]}
                    value={state[input] || form[input].value}
                  />
                </div>
              );
            })}
          </StyledRow>

          <Button type="submit" color="success" icon={<FontAwesomeIcon icon={faPlus} />}>{formatMessage({ id: getTrad('save') })}</Button>
        </form>
      </Block>
    </ContainerFluid>
  );
};

export default memo(HomePage);
