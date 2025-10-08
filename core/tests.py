from django.test import TestCase, Client
from django.urls import reverse

class CoreViewsTest(TestCase):
    
    def setUp(self):
        """
        Esta función se ejecuta antes de cada prueba.
        Aquí creamos un cliente para simular un navegador.
        """
        self.client = Client()

    def test_sobre_nosotros_page_loads_correctly(self):
        """
        Prueba que la página 'Sobre Nosotros' responde con un código 200 (OK).
        """
        # Obtenemos la URL usando su nombre, es más robusto que escribirla a mano
        url = reverse('sobre_nosotros')
        
        # El cliente simula una visita a esa URL
        response = self.client.get(url)
        
        # Verificamos que el código de estado de la respuesta sea 200
        self.assertEqual(response.status_code, 200)