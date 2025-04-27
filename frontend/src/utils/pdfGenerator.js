import jsPDF from 'jspdf';
import 'jspdf-autotable';

export const generarPDF = () => {
    const doc = new jsPDF();

    // Crear una tabla simple
    doc.autoTable({
        head: [['Columna 1', 'Columna 2', 'Columna 3']],
        body: [
            ['Dato 1', 'Dato 2', 'Dato 3'],
            ['Dato 4', 'Dato 5', 'Dato 6'],
            ['Dato 7', 'Dato 8', 'Dato 9'],
        ],
    });

    // Guardar el PDF
    doc.save('Tabla_De_Prueba.pdf');
};