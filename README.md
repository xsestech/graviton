# Graviton
 В данном репозитории представлен код математической модели первого гравитационного маневра около венеры аппарата Кассини-Гюйгенс.
## Структура проекта
В папке [src/](src/) находится весь основной код проекта. В [src/model](src/model) находится код модели, а в [src/KSP](src/KSP) находится код для снятия данных с KSP.
Также для удобства в папке [notebooks/](notebooks/) находится jupyter ноубуки с подробными комментариями:
- [trajectory_calulation.ipynb](notebooks/trajectory_calulation.ipynb) <html><a target="_blank" href="https://colab.research.google.com/github/xsestech/graviton/blob/master/notebooks/trajectory_calulation.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a></html>
- [plot_data.ipynb](notebooks/plot_data.ipynb)  <html><a target="_blank" href="https://colab.research.google.com/github/xsestech/graviton/blob/master/notebooks/plot_data.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a></html>

В папке [docs/](docs/) находится часть отчета и объяснения модели в latex. Посмотреть его в pdf можно с помощью [overleaf](https://ru.overleaf.com/project/6576264bef19b94f15c3d31d)

## Запуск проекта
### Клонируем репозиторий
```Shell
git clone https://github.com/xsestech/graviton.git
cd graviton
```
### Установка библиотек
```Shell
pip install -r requirements.txt
```
### Модель
Для начала работы перейдем в [папку с ее кодом](src/model).
```Shell
cd src/model
```
#### Конфигурация
Для изменения параметров нужно будет либо создать файл .env в [папке с моделью](src/model) c перечислением всех изменных параметров, либо изменить переменные среды. Пример .env:
```Dotenv
G=6.6743e-11
VENUS_R=700e3
VENUS_MASS:=1.2243980e23
PROBE_MASS= 600e3
V0=6.761e3
H0=251319
TIME_RANGE=3600
TIME_STEP=1e-2
METHOD=RK45
```
#### Запуск
```Shell
python3 model.py
```
### KSP
Для начала работы перейдем в [папку с ее кодом](src/KSP).
```Shell
cd src/model
```
#### Конфигурация
Для изменения параметров нужно будет либо создать файл .env в [папке с моделью](src/KSP) c перечислением всех изменных параметров, либо изменить переменные среды. Пример .env:
```Dotenv
DATA_PATH=../../data/
DATA_DELAY=0.1
WAIT_TIME=2
WARP_FACTOR=4
TARGET_PERIAPSIS=250e3
N_REQUESTS=1000
IS_CHEAT_ON=0
TIME_RANGE=1
N_SPLITS=10
```
#### Запуск вывода графиков
```Shell
python3 plot_data.py
```
#### Скрипта для снятия данных с KSP
```Shell
python3 plot_data.py
```
