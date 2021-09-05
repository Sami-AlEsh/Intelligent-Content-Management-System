import styled from 'styled-components';

const ContainerFluid = styled.div`
  padding: 18px 30px;
  > div:first-child {
    max-height: 33px;
  }
  .buttonOutline {
    height: 30px;
    padding: 0 15px;
    border: 1px solid #dfe0e1;
    font-weight: 500;
    font-size: 13px;
    &:before {
      margin-right: 10px;
      content: '\f08e';
      font-family: 'FontAwesome';
      font-size: 10px;
    }
  }
`;

const StyledRow = styled.div`
  padding-top: 11px;
  > div:last-child {
    > div {
      padding-bottom: 0 !important;
    }
  }
  > div:first-child {
    > div {
      margin-bottom: 22px !important;
    }
  }
`;

export { ContainerFluid, StyledRow };