import React from 'react';
import { Label } from '@buffetjs/core'
const InputMedia = ({
  disabled,
  label,
  onChange,
  name,
  attribute,
  value,
  type,
  id,
  error,
  labelIcon,
  placeholder
}) => {

  const handleChange = e => {
    onChange({ target: { name, type, value: e.target.files[0] } });
  };

  return (
    <>
      <Label htmlFor={name} message={label} />
      <input type="file"
        id={id} name={name}
        accept="image/*" onChange={handleChange} placeholder={placeholder} />

    </>
  )
}
export default InputMedia