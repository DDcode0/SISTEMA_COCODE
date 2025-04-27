import React, { useEffect, useState } from 'react';
import api from '../services/api';

const TablaCuotas = () => {
    const [cuotas, setCuotas] = useState([]);
    const [editCuota, setEditCuota] = useState(null);

    const fetchCuotas = async () => {
        try {
            const response = await api.get('/cuotas');
            setCuotas(response.data);
        } catch (error) {
            console.error('Error al obtener cuotas:', error);
            alert('No se pudieron cargar las cuotas.');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('¿Estás seguro de que deseas eliminar esta cuota?')) {
            try {
                await api.delete(`/cuotas/${id}`);
                setCuotas(cuotas.filter(cuota => cuota.ID_Cuota !== id));
                alert('Cuota eliminada exitosamente');
            } catch (error) {
                console.error('Error al eliminar la cuota:', error);
                alert('No se pudo eliminar la cuota.');
            }
        }
    };

    const handleUpdate = async () => {
        try {
            await api.put(`/cuotas/${editCuota.ID_Cuota}`, {
                Descripcion: editCuota.Descripcion,
                Monto: editCuota.Monto,
                Fecha_Limite: editCuota.Fecha_Limite,
            });
            setCuotas(cuotas.map(c =>
                c.ID_Cuota === editCuota.ID_Cuota ? editCuota : c
            ));
            setEditCuota(null);
            alert('Cuota actualizada exitosamente');
        } catch (error) {
            console.error('Error al actualizar la cuota:', error);
            alert('No se pudo actualizar la cuota.');
        }
    };

    useEffect(() => {
        fetchCuotas();
    }, []);

    return (
        <table className="table table-striped">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Descripción</th>
                    <th>Monto</th>
                    <th>Fecha Límite</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {cuotas.map((cuota, index) => (
                    <tr key={cuota.ID_Cuota}>
                        <td>{index + 1}</td>
                        <td>
                            {editCuota?.ID_Cuota === cuota.ID_Cuota ? (
                                <input
                                    type="text"
                                    value={editCuota.Descripcion}
                                    onChange={(e) =>
                                        setEditCuota({
                                            ...editCuota,
                                            Descripcion: e.target.value,
                                        })
                                    }
                                    className="form-control"
                                />
                            ) : (
                                cuota.Descripcion
                            )}
                        </td>
                        <td>
                            {editCuota?.ID_Cuota === cuota.ID_Cuota ? (
                                <input
                                    type="number"
                                    value={editCuota.Monto}
                                    onChange={(e) =>
                                        setEditCuota({
                                            ...editCuota,
                                            Monto: e.target.value,
                                        })
                                    }
                                    className="form-control"
                                />
                            ) : (
                                cuota.Monto
                            )}
                        </td>
                        <td>
                            {editCuota?.ID_Cuota === cuota.ID_Cuota ? (
                                <input
                                    type="date"
                                    value={editCuota.Fecha_Limite}
                                    onChange={(e) =>
                                        setEditCuota({
                                            ...editCuota,
                                            Fecha_Limite: e.target.value,
                                        })
                                    }
                                    className="form-control"
                                />
                            ) : (
                                cuota.Fecha_Limite
                            )}
                        </td>
                        <td>
                            {editCuota?.ID_Cuota === cuota.ID_Cuota ? (
                                <>
                                    <button
                                        className="btn btn-success btn-sm me-2"
                                        onClick={handleUpdate}
                                    >
                                        Guardar
                                    </button>
                                    <button
                                        className="btn btn-secondary btn-sm"
                                        onClick={() => setEditCuota(null)}
                                    >
                                        Cancelar
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        className="btn btn-primary btn-sm me-2"
                                        onClick={() => setEditCuota(cuota)}
                                    >
                                        Editar
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm"
                                        onClick={() => handleDelete(cuota.ID_Cuota)}
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

export default TablaCuotas;