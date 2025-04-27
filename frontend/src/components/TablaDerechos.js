import React, { useEffect, useState } from 'react';
import api from '../services/api';

const TablaDerechos = () => {
    const [derechos, setDerechos] = useState([]);
    const [editDerecho, setEditDerecho] = useState(null); // Derecho en edición

    const fetchDerechos = async () => {
        try {
            const response = await api.get('/derechos');
            setDerechos(response.data);
        } catch (error) {
            console.error('Error al obtener derechos:', error);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('¿Estás seguro de que deseas eliminar este derecho?')) {
            try {
                await api.delete(`/derechos/${id}`);
                setDerechos(derechos.filter(derecho => derecho.ID_Derecho !== id));
                alert('Derecho eliminado exitosamente');
            } catch (error) {
                console.error('Error al eliminar el derecho:', error);
                alert('No se pudo eliminar el derecho');
            }
        }
    };

    const handleUpdate = async () => {
        try {
            await api.put(`/derechos/${editDerecho.ID_Derecho}`, { Nombre: editDerecho.Nombre });
            setDerechos(derechos.map(d =>
                d.ID_Derecho === editDerecho.ID_Derecho ? editDerecho : d
            ));
            setEditDerecho(null); // Salir de la edición
            alert('Derecho actualizado exitosamente');
        } catch (error) {
            console.error('Error al actualizar el derecho:', error);
            alert('No se pudo actualizar el derecho');
        }
    };

    useEffect(() => {
        fetchDerechos();
    }, []);

    return (
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Nombre</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {derechos.map((derecho, index) => (
                    <tr key={derecho.ID_Derecho}>
                        <td>{index + 1}</td>
                        <td>
                            {editDerecho?.ID_Derecho === derecho.ID_Derecho ? (
                                <input
                                    type="text"
                                    value={editDerecho.Nombre}
                                    onChange={(e) =>
                                        setEditDerecho({
                                            ...editDerecho,
                                            Nombre: e.target.value,
                                        })
                                    }
                                    className="form-control"
                                />
                            ) : (
                                derecho.Nombre
                            )}
                        </td>
                        <td>
                            {editDerecho?.ID_Derecho === derecho.ID_Derecho ? (
                                <>
                                    <button
                                        className="btn btn-success btn-sm me-2"
                                        onClick={handleUpdate}
                                    >
                                        Guardar
                                    </button>
                                    <button
                                        className="btn btn-secondary btn-sm"
                                        onClick={() => setEditDerecho(null)}
                                    >
                                        Cancelar
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        className="btn btn-primary btn-sm me-2"
                                        onClick={() => setEditDerecho(derecho)}
                                    >
                                        Editar
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() => handleDelete(derecho.ID_Derecho)}
                                    >
                                        Eliminar
                                    </button>
                                </>
                            )}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default TablaDerechos;