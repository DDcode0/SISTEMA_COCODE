import React from 'react';

export default function AlertList({ errores = [], success }) {
  return (
    <>
      {success && (
        <div className="alert alert-success" role="alert">
          {success}
        </div>
      )}
      {errores.length > 0 && (
        <div className="alert alert-danger">
          <ul className="mb-0">
            {errores.map((e,i) => <li key={i}>{e}</li>)}
          </ul>
        </div>
      )}
    </>
  );
}
