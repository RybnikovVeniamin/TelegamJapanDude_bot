from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
import json
from datetime import datetime
import re
from pydub import AudioSegment

app = Flask(__name__)

# Папка для сохранения записей
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """Анализирует аудио файл и возвращает рекомендации"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file'}), 400
        
        audio_file = request.files['audio']
        
        # Сохраняем временный файл с оригинальным расширением
        timestamp = datetime.now().timestamp()
        original_path = os.path.join(RECORDINGS_DIR, f"temp_{timestamp}")
        audio_file.save(original_path)
        
        # Конвертируем в WAV формат для распознавания речи
        wav_path = os.path.join(RECORDINGS_DIR, f"temp_{timestamp}.wav")
        try:
            # Определяем формат по расширению файла или пробуем разные форматы
            audio = AudioSegment.from_file(original_path)
            audio.export(wav_path, format="wav")
            os.remove(original_path)  # Удаляем оригинальный файл
        except Exception as e:
            # Если конвертация не удалась, пробуем использовать файл как есть
            if os.path.exists(original_path):
                os.rename(original_path, wav_path)
            else:
                wav_path = original_path
        
        # Распознаем речь
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
        
        try:
            # Используем Google Speech Recognition (работает онлайн)
            text = recognizer.recognize_google(audio_data, language='en-US')
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f'Recognition service error: {str(e)}'}), 500
        
        # Анализируем текст
        analysis = analyze_text(text)
        
        # Удаляем временный файл
        if os.path.exists(wav_path):
            os.remove(wav_path)
        
        return jsonify({
            'transcription': text,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_text(text):
    """Анализирует текст на грамматические ошибки и дает рекомендации"""
    recommendations = []
    issues = []
    
    # Базовые проверки грамматики (можно расширить)
    
    # Проверка на повторяющиеся слова
    words = text.lower().split()
    repeated_words = []
    for i in range(len(words) - 1):
        if words[i] == words[i + 1] and words[i] not in repeated_words:
            repeated_words.append(words[i])
            issues.append({
                'type': 'repetition',
                'word': words[i],
                'message': f'Повторяющееся слово: "{words[i]}"'
            })
    
    # Проверка на длинные предложения
    sentences = re.split(r'[.!?]+', text)
    for i, sentence in enumerate(sentences):
        if len(sentence.split()) > 25:
            issues.append({
                'type': 'long_sentence',
                'sentence_num': i + 1,
                'message': f'Длинное предложение (больше 25 слов). Попробуйте разбить на несколько.'
            })
    
    # Проверка на общие ошибки произношения
    pronunciation_tips = []
    
    # Подсчет filler words (можно улучшить)
    filler_words = ['um', 'uh', 'like', 'you know', 'so', 'well']
    filler_count = sum(text.lower().count(word) for word in filler_words)
    if filler_count > 3:
        issues.append({
            'type': 'filler_words',
            'count': filler_count,
            'message': f'Много слов-паразитов ({filler_count}). Попробуйте говорить более уверенно и делать паузы вместо "um" и "uh".'
        })
    
    # Рекомендации по произношению
    pronunciation_tips.append({
        'tip': 'Говорите четко и не торопитесь. Делайте паузы между предложениями.'
    })
    
    pronunciation_tips.append({
        'tip': 'Обратите внимание на ударения в словах. Читайте вслух для практики.'
    })
    
    # Подготовка общего результата
    score = max(0, 100 - len(issues) * 10)
    
    return {
        'score': score,
        'issues': issues,
        'pronunciation_tips': pronunciation_tips,
        'word_count': len(words),
        'sentence_count': len([s for s in sentences if s.strip()])
    }

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

