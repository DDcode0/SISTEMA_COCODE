import React, { useState, useEffect } from 'react';
import api from '../services/api';

const TablaPersonas = () => {
    const [personas, setPersonas] = useState([]);
    const [personaSeleccionada, setPersonaSeleccionada] = useState(null); // Persona para editar
    const [mostrarModal, setMostrarModal] = useState(false); // Control del modal

    useEffect(() => {
        const fetchPersonas = async () => {
            try {
                const response = await api.get('/personas');
                setPersonas(response.data);
            } catch (error) {
                console.error('Error al obtener personas:', error);
            }
        };
        fetchPersonas();
    }, []);

    useEffect(() => {
        console.log('El estado de mostrarModal es:', mostrarModal);
    }, [mostrarModal]);

    const handleEdit = (persona) => {
        console.log('Persona seleccionada:', persona); // Rastrea la persona seleccionada
        setPersonaSeleccionada(persona); // Guardar la persona seleccionada
        console.log('Antes de cambiar mostrarModal:', mostrarModal);

        setMostrarModal(true); // Mostrar el modal
        console.log('Modal debería abrirse:', mostrarModal);
    };

    const handleUpdate = async () => {
        // Validación básica
        if (!personaSeleccionada.Nombre || !personaSeleccionada.DPI || !personaSeleccionada.Email) {
            alert('Por favor, complete todos los campos obligatorios.');
            return;
        }
        
        try {
            await api.put(`/personas/${personaSeleccionada.ID_Persona}`, personaSeleccionada);
            setPersonas(personas.map((p) =>
                p.ID_Persona === personaSeleccionada.ID_Persona ? personaSeleccionada : p
            ));
            setMostrarModal(false); // Cerrar el modal
        } catch (error) {
            console.error('Error al actualizar persona:', error);
            alert('Hubo un error al actualizar la persona.');
        }
    };

    const handleDelete = async (id) => {
        const confirmacion = window.confirm('¿Estás seguro de que deseas eliminar este registro?');
        if (confirmacion) {
            try {
                await api.delete(`/personas/${id}`);
                setPersonas(personas.filter((persona) => persona.ID_Persona !== id)); // Actualizar la tabla
            } catch (error) {
                console.error('Error al eliminar persona:', error);
            }
        }
    };

    return (
        <div>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>DPI</th>
                        <th>Nombre</th>
                        <th>Rol</th>
                        <th>Email</th>
                        <th>Teléfono</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {personas.map((persona, index) => (
                        <tr key={persona.ID_Persona}>
                            <td>{index + 1}</td>
                            <td>{persona.DPI}</td>
                            <td>{persona.Nombre}</td>
                            <td>{persona.Rol}</td>
                            <td>{persona.Email}</td>
                            <td>{persona.Telefono}</td>
                            <td>
                            <button
                                    className="btn btn-primary btn-sm me-2"
                                    onClick={() => handleEdit(persona)} // Verifica que está pasando la persona a la función
                                >
                                    Editar
                                </button>
                                <button
                                    className="btn btn-danger btn-sm"
                                    onClick={() => handleDelete(persona.ID_Persona)}
                                >
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Modal para editar */}
            {mostrarModal && (
         

                <div className="modal">
                    <div className="modal-content">
                        <h2>Editar Persona</h2>
                        <div className="mb-3">
                            <label>DPI:</label>
                            <input
                                type="text"
                                value={personaSeleccionada?.DPI || ''}
                                onChange={(e) =>
                                    setPersonaSeleccionada({
                                        ...personaSeleccionada,
                                        DPI: e.target.value,
                                    })
                                }
                                className="form-control"
                            />
                        </div>
                        <div className="mb-3">
                            <label>Nombre:</label>
                            <input
                                type="text"
                                value={personaSeleccionada?.Nombre || ''}
                                onChange={(e) =>
                                    setPersonaSeleccionada({
                                        ...personaSeleccionada,
                                        Nombre: e.target.value,
                                    })
                                }
                                className="form-control"
                            />
                        </div>
                        <div className="mb-3">
                            <label>Rol:</label>
                            <select
                                value={personaSeleccionada?.Rol || ''}
                                onChange={(e) =>
                                    setPersonaSeleccionada({
                                        ...personaSeleccionada,
                                        Rol: e.target.value,
                                    })
                                }
                                className="form-control"
                            >
                                <option value="Presidente">Presidente</option>
                                <option value="Vicepresidente">Vicepresidente</option>
                                <option value="Secretario">Secretario</option>
                                <option value="Tesorero">Tesorero</option>
                                <option value="Vocal I">Vocal I</option>
                                <option value="Vocal II">Vocal II</option>
                                <option value="Vocal III">Vocal III</option>
                                <option value="Sin rol">Sin rol</option>
                            </select>
                        </div>
                        <div className="mb-3">
                            <label>Email:</label>
                            <input
                                type="email"
                                value={personaSeleccionada?.Email || ''}
                                onChange={(e) =>
                                    setPersonaSeleccionada({
                                        ...personaSeleccionada,
                                        Email: e.target.value,
                                    })
                                }
                                className="form-control"
                            />
                        </div>
                        <div className="mb-3">
                            <label>Teléfono:</label>
                            <input
                                type="text"
                                value={personaSeleccionada?.Telefono || ''}
                                onChange={(e) =>
                                    setPersonaSeleccionada({
                                        ...personaSeleccionada,
                                        Telefono: e.target.value,
                                    })
                                }
                                className="form-control"
                            />
                        </div>
                        <button className="btn btn-success me-2" onClick={handleUpdate}>
                            Guardar Cambios
                        </button>
                        <button className="btn btn-secondary" onClick={() => setMostrarModal(false)}>
                            Cancelar
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TablaPersonas;