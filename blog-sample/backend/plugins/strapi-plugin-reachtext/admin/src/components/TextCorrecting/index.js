import { Button } from '@buffetjs/core';
import { faSpellCheck } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Modal, ModalFooter, PopUpWarning, useGlobalContext, request } from 'strapi-helper-plugin';
import PropTypes from 'prop-types';
import React, { useState } from 'react';
import { fetchTextCorrections } from '../../utils/fetchCorrections';
import styled from 'styled-components';
import getTrad from '../../utils/getTrad';

const Wrapper = styled.div`
  padding: .5rem;
`;

const List = styled.dl`
    overflow-y: auto;
    max-height: 23rem;
    >p dt{
    color: #222;
    font-size: 14px;
    font-weight: normal;
    text-transform: uppercase;
  },
  >p:nth-child(n+2) {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #e5e5e5;
  }
`

const TextCorrecting = ({ value }) => {
  const { emitEvent, formatMessage } = useGlobalContext();
  const [corrections, setCorrections] = useState([]);

  const fetchCorrections = () => {
    if (value != null && value != undefined) {
      fetchTextCorrections(value).then(response => {
        setCorrections([...response.data.words]);
      });
    }
  }

  return (
    <Wrapper>
      <Button onClick={fetchCorrections} color="primary" icon={<FontAwesomeIcon icon={faSpellCheck} />}>{formatMessage({ id: getTrad('spell.checking') })}</Button>

      {(corrections?.length != 0) &&
        (<List className="uk-description-list uk-description-list-divider">
          {corrections.filter(wordCorrection => wordCorrection.word.length > 2 && wordCorrection.correction.length > 0).map((wordCorrection, id) => (
            <p key={id}>
              <dt>{wordCorrection.word}</dt>
              <dd>{wordCorrection.correction.join(', ')}</dd>
            </p>
          ))}
        </List>)
      }
    </Wrapper>
  )
}

TextCorrecting.defaultProps = {
  value: ''
}

TextCorrecting.propTypes = {
  value: PropTypes.string,
}
export default TextCorrecting;