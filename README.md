# Spotify Plan Checker 🎶

## Descripción extendida

Este proyecto permite comprobar el estado de las cuentas de Spotify mediante archivos de cookies, categorizando cada cuenta según su plan (Ej. Premium, Familiar, Estudiante, etc.). Utiliza múltiples hilos para agilizar el proceso y organizar los resultados en directorios por tipo de plan. 🗂️

### Funcionalidades principales:

✨ **Verificación de planes**: Determina automáticamente el tipo de suscripción de una cuenta (Ej. Premium, Estudiante, Familiar).  
✨ **Organización de resultados**: Los resultados se guardan en directorios correspondientes a cada tipo de plan.  
✨ **Multihilo**: Utiliza múltiples hilos (hasta 100) para procesar las cuentas de manera simultánea, mejorando la eficiencia.  
✨ **Interfaz amigable**: Resultados mostrados en colores y con un banner divertido. 😄  
✨ **Sin necesidad de proxies**: Todo funciona de manera local, sin necesidad de configurar proxies, ideal para proyectos pequeños o pruebas rápidas.

## Requisitos

Para usar este script, necesitas tener Python 3.7 o superior y las siguientes dependencias:

- `requests`
- `colorama`
- `threading`
- `sys`
- `concurrent.futures`

Puedes instalar las dependencias usando:

```bash
pip install requests colorama
```
![{F0B0388C-2CBB-47E7-A847-D59636D6E57C}](https://github.com/user-attachments/assets/d939678c-673e-439e-8b08-8c1c71f8faba)

![45A6DB42-1C45-4F08-93A4-8D3C8A9C9137](https://github.com/user-attachments/assets/8e1e8829-33e5-4cfd-8f36-d20928e2bfbd)

Inspirado en: https://github.com/harshitkamboj/Spotify-Cookie-Checker
