
const precio_c_m_c = 120;
const precio_t_c = 250;
const precio_e_d = 150;
function calculadora(constante) {
        switch (constante) {
                case 'c_m_c':
                        let n1 = parseFloat(document.getElementById('n1').value)
                        let resultado = n1 * precio_c_m_c
                        document.getElementById('resultado').value = resultado
                        break;
                case 't_c':
                        let n2 = parseFloat(document.getElementById('n2').value)
                        let resultado2 = n2 * precio_t_c
                        document.getElementById('resultado2').value = resultado2
                        break;
                case 'e_d':
                        let n3 = parseFloat(document.getElementById('n3').value)
                        let resultado3 = n3 * precio_e_d
                        document.getElementById('resultado3').value = resultado3
                        break;
        }
}

function limpiar(constante) {
        switch (constante) {
                case 'c_m_c':
                        document.getElementById('n1').value = ''
                        document.getElementById('resultado').value = ''
                        break;
                case 't_c':
                        document.getElementById('n2').value = ''
                        document.getElementById('resultado2').value = ''
                        break;
                case 'e_d':
                        document.getElementById('n3').value = ''
                        document.getElementById('resultado3').value = ''
                        break;
        }
}
