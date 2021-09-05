import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import React, { useEffect, useState } from 'react';
import {
  useContentManagerEditViewDataManager
} from 'strapi-helper-plugin';
import styled from 'styled-components';
import { fetchAutoTags } from '../../utils/fetchTags';
import { arrayFromString, arrayToString } from '../../utils/transporter';

const InputWrapper = styled.div`
  display: grid;
  align-items:center;
  grid-template-columns: 10fr 1fr;
`;

const InputButton = styled.span`
  min-width: 7.9rem;
  height: 5rem;
  margin-top: 0.9rem;
  background-color: rgba(16,22,34,0.02);
  border: 1px solid #e3e9f3;
  border-left: 0;
  border-radius: 0.25rem;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  color: rgba(16,22,34,0.5);
  line-height: 5rem;
  font-size: 1.3rem;
  font-family: 'Lato';
  font-weight: 600 !important;
  -moz-appearance: none;
  -webkit-appearance: none;
  text-align: center;
  cursor: pointer;
`;


export default function GenerateTags({ autoFocus, inputDescription, disabled, error, name, label, value, placeholder, onBlur, onChange, attribute },) {
  const [options, setOptions] = useState(["..."]);
  const [loading, setLoading] = useState(false);
  const { modifiedData } = useContentManagerEditViewDataManager()

  useEffect(() => {
    fetchTags();
  }, [])

  const fetchTags = () => {
    if (modifiedData[attribute.relatedText] != null && modifiedData[attribute.relatedText] != undefined) {
      setLoading(true);
      fetchAutoTags(modifiedData[attribute.relatedText]).then((response) => {
        setOptions(response.data.tags);
        setLoading(false);
      })
    }
  }

  const handleChangeTags = (event, values) => {
    // console.log(values)
    onChange({ target: { value: arrayToString(values), name, type: 'text' } })
  }
  return (
    <InputWrapper className="">
      {/* <Label
        htmlFor={name}
        message={label}
      /> */}
      <Autocomplete
        multiple
        options={options}
        disabled={disabled}
        freeSolo
        defaultValue={[]}
        value={arrayFromString(value)}
        onChange={handleChangeTags}
        renderInput={params => (
          <TextField
            {...params}
            variant="outlined"
            label={name}
            placeholder={placeholder}
            margin="normal"
            fullWidth
          />
        )}></Autocomplete>
      {/* <Button color="success" onClick={fetchAutoTags} icon={<FontAwesomeIcon icon={faPlus} />}>refresh</Button> */}
      <InputButton onClick={fetchTags} style={{ 'pointerEvents': loading ? 'none' : 'auto' }}>
        {/* <i className="fas fa-redo" role="button" aria-hidden="true" /> */}
        {!loading ? "Generate" : "Generating ..."}
      </InputButton>
    </InputWrapper>
  );
}