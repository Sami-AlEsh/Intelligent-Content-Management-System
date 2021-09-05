import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { Label, Button } from '@buffetjs/core'
import { postPdfOCR } from '../../utils/postPdfOcr';
import { Modal, ModalFooter, PopUpWarning, useGlobalContext, request } from 'strapi-helper-plugin';
import getTrad from '../../utils/getTrad';

const Wrapper = styled.div`
  padding: 1.5rem .5rem;
  direction: rtl
`;


const OCRPdf = ({
  onGetContent,
}) => {
  const { emitEvent, formatMessage } = useGlobalContext();

  const pdfFileInputRef = useRef(null);

  const handleChange = e => {
    // onChange({ target: { name, type, value: e.target.files[0] } });
    postPdfOCR(e.target.files[0]).then(result => {
      const pdfContent = result.data.text;
      onGetContent(pdfContent);
      pdfFileInputRef.current.value = "";
      strapi.notification.success("pdf content inserted successfully");
    });
  };

  const onButtonClick = () => {
    pdfFileInputRef.current.click();
  }

  return (
    <Wrapper>
      <Label htmlFor="ocd-pdf-file" message={formatMessage({ id: getTrad('choose.pdf') })} />
      <input ref={pdfFileInputRef} type="file"
        id="ocd-pdf-file" name="ocd-pdf-file"
        hidden
        accept="application/pdf" onChange={handleChange} />
      <Button color="secondary" onClick={onButtonClick}>{formatMessage({ id: getTrad('pick.pdf') })}</Button>

    </Wrapper>
  )
}

export default OCRPdf;