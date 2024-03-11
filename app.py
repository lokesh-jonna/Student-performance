from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def calculate_performance(scores, attendance):
    average_score = np.mean(scores)
    overall_performance = calculate_grade(average_score)
    suggestions = generate_suggestions(attendance)
    return overall_performance, suggestions

def calculate_grade(average_score):
    if average_score >= 90:
        return 'A'
    elif 80 <= average_score < 90:
        return 'B'
    elif 70 <= average_score < 80:
        return 'C'
    elif 60 <= average_score < 70:
        return 'D'
    else:
        return 'F'

def generate_suggestions(attendance):
    if attendance < 75:
        return "Your attendance is low. Try to improve it for better performance."
    else:
        return "Your attendance is good. Keep up the good work!"

def generate_plot(data, plot_type='bar'):
    plt.switch_backend('Agg')  # To prevent opening window while running without GUI
    plt.figure(figsize=(6, 4))
    if plot_type == 'bar':
        plt.bar(range(len(data)), data)
    elif plot_type == 'pie':
        plt.pie(data, labels=['Pass', 'Fail'], autopct='%1.1f%%')
    plt.xlabel('Categories')
    plt.ylabel('Scores')
    plt.title('Subject Performance')
    plt.tight_layout()

    # Convert plot to PNG image and encode as base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return plot_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        subject1 = int(request.form['subject1'])
        subject2 = int(request.form['subject2'])
        subject3 = int(request.form['subject3'])
        subject4 = int(request.form['subject4'])
        subject5 = int(request.form['subject5'])
        attendance = int(request.form['attendance'])

        scores = [subject1, subject2, subject3, subject4, subject5]
        overall_performance, suggestions = calculate_performance(scores, attendance)

        # Generate plots for each subject
        subject_names = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']
        subject_plots = [generate_plot([score, 100-score], plot_type='pie') for score in scores]

        # Generate overall performance histogram
        overall_performance_plot = generate_plot(scores)

        # Generate attendance plot
        attendance_plot = generate_plot([attendance, 100-attendance], plot_type='pie')

        return render_template('results.html', name=name, overall_performance=overall_performance,
                               suggestions=suggestions, subject_names=subject_names,
                               subject_plots=subject_plots, overall_performance_plot=overall_performance_plot,
                               attendance_plot=attendance_plot)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
