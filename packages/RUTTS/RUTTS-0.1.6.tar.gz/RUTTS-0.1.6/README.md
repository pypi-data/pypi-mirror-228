# Russian TTS inference
# Установка
**1)Установка пакета:**

  **a) скачать из pypi: pip install RUTTS**
  
  **b) из гита (нужен установленный гит) pip install -e git+https://github.com/Tera2Space/RUTTS#egg=RUTTS**
# Ошибки
1)Если на винде у вас **ошибка при установке**,нужно просто **скачать Visual Studio [здесь](https://visualstudio.microsoft.com/ru/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false)** и при установке выбрать галочку около **Разработка классических приложений на С++**

2)Если **после установки не работает** что-то, **убедитесь что модуль скачан последней версии**(удалить и скачать) и **так же что названия моделей есть на** https://huggingface.co/TeraTTS
# Использование

```python  
  from RUTTS import TTS
  
  # Cоздать модель по имени
  #P.S все модели https://huggingface.co/TeraTTS P.S там есть модель для GLADOS
  tts = TTS("TeraTTS/natasha-g2p-vits") # Можно передать параметр add_time_to_end (по умолчанию = 0.8) это кол-во добавленных секунд в аудио для хорошего звучания
  
  audio = tts("что делаешь?", lenght_scale=1.2) # Создать аудио. Можно ставить ударения используя +. lenght_scale - замедлить аудио для хорошего звучания, параметр по умолчанию передается как 1.2, указан для примера
  
  tts.play_audio(audio) # Проиграть созданное аудио
  tts("пока!", play=True) # Создать аудио и сразу проиграть его
  
  tts.save_wav(audio, "./test.wav") # Сохранить аудио
```
