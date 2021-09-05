import React, { useRef, useState } from 'react';
import {
  ButtonModal, Modal, ModalBody as modalBody, ModalFooter, ModalHeader
} from 'strapi-helper-plugin';
import styled from 'styled-components';
import { Input } from './Input';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';


const ModalBody = styled(modalBody)`
  .row {
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
`;

const arrayToString = (arr) => arr.join(',');
const arrayFromString = (str) => str.split(',');

export function LassoModal({ isOpen, value, onConfirm, onDismiss, onToggle }) {
  const [lassoValue, setLassoValue] = useState([]);
  const lastValue = useRef(value);
  const wasOpen = useRef(isOpen);

  if (value !== lastValue.current || isOpen !== wasOpen.current) {
    wasOpen.current = isOpen;
    lastValue.current = value;
    setLassoValue(arrayFromString(value));
  }

  return (
    <Modal isOpen={isOpen} onToggle={onToggle}>
      <ModalHeader
        onClickGoBack={onToggle}
        HeaderComponent={() => <p>check the tags tou can update them as you like</p>}
      />
      <ModalBody style>
        {
          lassoValue.map((val, id) => {
            return <Autocomplete
              key={id}
              id={`${id}`}
              freeSolo
              options={[
                "Alligator",
                "Bask",
                "Crocodilian",
                "Death Roll",
                "Eggs",
                "Jaws",
                "Reptile",
                "Solitary",
                "Tail",
                "Wetlands"
              ]}
              renderInput={(params) => (
                <TextField {...params} label="Combo box" variant="outlined" />
              // <div ref={params.inputProps.ref}>
                //   <Input
                //     name={`${id}`}
                //     placeholder={"enter tag"}
                //     value={val || ''}
                //     disabled={false}
                //     onClick={() => {
                //       // setLassoModalOpen(true);
                //       if (id == 0) {// handle add new tag
                //         setLassoValue([...lassoValue, '']);
                //       } else {// handle delete tag
                //         setLassoValue([...lassoValue.slice(0, id), ...lassoValue.slice(id + 1)]);
                //       }
                //     }}
                //     onChange={(newVal) => {
                //       var values = lassoValue.slice();
                //       values[id] = newVal;
                //       setLassoValue(values);
                //     }}
                //     icon={id == 0 ? 'fas fa-plus' : 'fas fa-times'}
                //     {...params.inputParams}
                //   />
                // </div>
              )}
            />
            // return <Input
            //   key={id}
            //   name={`${id}`}
            //   placeholder={"enter tag"}
            //   value={val || ''}
            //   disabled={false}
            //   onClick={() => {
            //     // setLassoModalOpen(true);
            //     if (id == 0) {// handle add new tag
            //       setLassoValue([...lassoValue, '']);
            //     } else {// handle delete tag
            //       setLassoValue([...lassoValue.slice(0, id), ...lassoValue.slice(id + 1)]);
            //     }
            //   }}
            //   onChange={(newVal) => {
            //     var values = lassoValue.slice();
            //     values[id] = newVal;
            //     setLassoValue(values);
            //   }}
            //   icon={id == 0 ? 'fas fa-plus' : 'fas fa-times'}
            // />
            // <h2 key={id}>{val}</h2>
          })
        }
      </ModalBody>
      <ModalFooter>
        <section>
          <ButtonModal message="app.components.Button.cancel" isSecondary={true} onClick={() => {
            onToggle();
            onDismiss();
          }} />
          {/* <ButtonModal message="plugin.Button.generate" isSecondary={false} onClick={() => {
            onToggle();
            onConfirm(arrayToString(lassoValue));
          }} /> */}
          <ButtonModal message="app.components.Button.save" isSecondary={false} onClick={() => {
            onToggle();
            onConfirm(arrayToString(lassoValue));
          }} />
        </section>
      </ModalFooter>
    </Modal>
  );
}

LassoModal.defaultProps = {
  onConfirm: () => { },
  onDismiss: () => { }
};
