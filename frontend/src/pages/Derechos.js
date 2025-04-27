import React from 'react';
import FormDerechos from '../components/FormDerechos';
import TablaDerechos from '../components/TablaDerechos';

const Derechos = () => {
    return (
        <div className="container">
            <h1>Gestión de Derechos</h1>
            <div className="mb-4">
                <FormDerechos onSuccess={() => window.location.reload()} /> {/* Recarga al crear */}
            </div>
            <TablaDerechos />
        </div>
    );
};

export default Derechos;