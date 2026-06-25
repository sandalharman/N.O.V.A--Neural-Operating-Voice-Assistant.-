import sys, time, numpy as np, sounddevice as sd
from PyQt6.QtCore import Qt,QThread,pyqtSignal,QTimer,QRectF
from PyQt6.QtGui import QPainter,QColor,QPen,QFont,QLinearGradient
from PyQt6.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QTextEdit,QLineEdit,QFrame
from config import ASSISTANT_NAME,CLAP_THRESHOLD,CLAPS_TO_WAKE
from commands import handle_command
from speech_io import listen_once
from tts_engine import speak
APP_STYLE="""
QWidget{background-color:#02070d;color:#e9fbff;font-family:Segoe UI;} QFrame#Panel{background-color:rgba(8,20,32,230);border:1px solid rgba(112,244,255,70);border-radius:24px;} QTextEdit{background-color:rgba(1,8,14,220);border:1px solid rgba(112,244,255,70);border-radius:16px;padding:14px;color:#e9fbff;font-size:14px;} QLineEdit{background-color:rgba(1,8,14,230);border:1px solid rgba(112,244,255,80);border-radius:14px;padding:12px;color:#e9fbff;font-size:15px;} QPushButton{background-color:rgba(0,234,255,35);border:1px solid rgba(0,234,255,120);border-radius:14px;padding:11px 18px;color:#e9fbff;font-weight:bold;} QPushButton:hover{background-color:rgba(0,234,255,70);} QLabel#Title{font-size:38px;font-weight:900;letter-spacing:7px;color:#e9fbff;} QLabel#SubTitle{color:#89aeb8;font-size:12px;} QLabel#Status{color:#00eaff;font-size:14px;font-weight:bold;}
"""
class OrbWidget(QWidget):
    def __init__(self): super().__init__(); self.angle=0; self.setMinimumSize(320,320); self.timer=QTimer(self); self.timer.timeout.connect(self.animate); self.timer.start(30)
    def animate(self): self.angle=(self.angle+2)%360; self.update()
    def paintEvent(self,event):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing); r=self.rect(); p.translate(r.width()/2,r.height()/2)
        for radius,offset,alpha in [(145,0,180),(118,80,140),(92,160,110)]:
            p.save(); p.rotate(self.angle+offset); p.setPen(QPen(QColor(0,234,255,alpha),2)); p.drawArc(QRectF(-radius,-radius,radius*2,radius*2),20*16,290*16); p.restore()
        g=QLinearGradient(-60,-60,60,60); g.setColorAt(0,QColor(0,234,255,90)); g.setColorAt(1,QColor(0,50,70,80)); p.setBrush(g); p.setPen(QPen(QColor(0,234,255,220),2)); p.drawEllipse(QRectF(-70,-70,140,140))
        p.setPen(QColor(233,251,255)); p.setFont(QFont('Segoe UI',22,QFont.Weight.Bold)); p.drawText(QRectF(-70,-25,140,35),Qt.AlignmentFlag.AlignCenter,ASSISTANT_NAME)
        p.setPen(QColor(137,174,184)); p.setFont(QFont('Segoe UI',8,QFont.Weight.Bold)); p.drawText(QRectF(-70,12,140,25),Qt.AlignmentFlag.AlignCenter,'ONLINE')
class Worker(QThread):
    finished_text=pyqtSignal(str); status_text=pyqtSignal(str)
    def __init__(self,text=None,voice=False): super().__init__(); self.text=text; self.voice=voice
    def run(self):
        try:
            if self.voice:
                self.status_text.emit('LISTENING'); speak('Yes, I am listening.'); text=listen_once()
                if not text: self.finished_text.emit('I did not catch that.'); return
                self.status_text.emit('THINKING'); reply=handle_command(text); self.finished_text.emit('USER:'+text+'\nNOVA:'+reply); speak(reply)
            else:
                self.status_text.emit('THINKING'); reply=handle_command(self.text); self.finished_text.emit(reply); speak(reply)
        except Exception as e: self.finished_text.emit('Error: '+str(e))
        finally: self.status_text.emit('ONLINE')
class ClapThread(QThread):
    woke=pyqtSignal()
    def run(self):
        clap_times=[]; cooldown=0.25; last_clap=0
        def cb(indata,frames,time_info,status):
            nonlocal clap_times,last_clap
            vol=float(np.linalg.norm(indata)); now=time.time()
            if vol>CLAP_THRESHOLD and now-last_clap>cooldown:
                last_clap=now; clap_times.append(now); clap_times=[t for t in clap_times if now-t<1.5]
                if len(clap_times)>=CLAPS_TO_WAKE: clap_times=[]; self.woke.emit()
        try:
            with sd.InputStream(callback=cb,channels=1,samplerate=44100):
                while True: time.sleep(0.1)
        except Exception: pass
class NovaDesktop(QWidget):
    def __init__(self):
        super().__init__(); self.setWindowTitle('NOVA - Desktop AI Assistant'); self.setMinimumSize(1100,700); self.setStyleSheet(APP_STYLE)
        self.status=QLabel('ONLINE'); self.status.setObjectName('Status'); self.chat=QTextEdit(); self.chat.setReadOnly(True); self.chat.setText('NOVA: System online. Clap twice, press Mic, or type a command.\n')
        self.input=QLineEdit(); self.input.setPlaceholderText('Ask NOVA anything...'); self.input.returnPressed.connect(self.send_text); self.build_ui(); self.clap_thread=ClapThread(); self.clap_thread.woke.connect(self.listen_voice); self.clap_thread.start(); speak(f'{ASSISTANT_NAME} desktop assistant is online.')
    def build_ui(self):
        root=QHBoxLayout(self); root.setContentsMargins(22,22,22,22); root.setSpacing(20)
        left=QFrame(); left.setObjectName('Panel'); ll=QVBoxLayout(left); ll.setContentsMargins(24,24,24,24)
        title=QLabel(ASSISTANT_NAME); title.setObjectName('Title'); sub=QLabel('Neural Operating Voice Assistant'); sub.setObjectName('SubTitle'); ll.addWidget(title); ll.addWidget(sub); ll.addSpacing(20); ll.addWidget(OrbWidget(),alignment=Qt.AlignmentFlag.AlignCenter); ll.addStretch(); ll.addWidget(QLabel('STATUS')); ll.addWidget(self.status); ll.addSpacing(12); help_box=QLabel('Wake: clap twice\nBrain: Ollama Local AI\nMode: Desktop App'); help_box.setObjectName('SubTitle'); ll.addWidget(help_box)
        right=QFrame(); right.setObjectName('Panel'); rl=QVBoxLayout(right); rl.setContentsMargins(24,24,24,24); rl.setSpacing(14); header=QLabel('COMMAND INTERFACE'); header.setObjectName('Title'); header.setStyleSheet('font-size:24px;letter-spacing:3px;'); rl.addWidget(header); rl.addWidget(self.chat,stretch=1)
        row=QHBoxLayout(); mic=QPushButton('🎤 Mic'); mic.clicked.connect(self.listen_voice); send=QPushButton('Send'); send.clicked.connect(self.send_text); clear=QPushButton('Clear'); clear.clicked.connect(self.chat.clear); row.addWidget(mic); row.addWidget(self.input,stretch=1); row.addWidget(send); row.addWidget(clear); rl.addLayout(row)
        qrow=QHBoxLayout()
        for label,cmd in [('System','system status'),('YouTube','open youtube'),('Screenshot','take screenshot'),('Help','what can you do')]:
            b=QPushButton(label); b.clicked.connect(lambda checked=False,c=cmd:self.quick(c)); qrow.addWidget(b)
        rl.addLayout(qrow); root.addWidget(left,stretch=3); root.addWidget(right,stretch=7)
    def append_chat(self,speaker,text): self.chat.append(f'\n{speaker}: {text}'); self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())
    def set_status(self,text): self.status.setText(text)
    def quick(self,text): self.input.setText(text); self.send_text()
    def send_text(self):
        text=self.input.text().strip()
        if not text: return
        self.input.clear(); self.append_chat('YOU',text); self.worker=Worker(text=text); self.worker.status_text.connect(self.set_status); self.worker.finished_text.connect(lambda reply:self.append_chat('NOVA',reply)); self.worker.start()
    def listen_voice(self): self.worker=Worker(voice=True); self.worker.status_text.connect(self.set_status); self.worker.finished_text.connect(self.handle_voice_reply); self.worker.start()
    def handle_voice_reply(self,text):
        if text.startswith('USER:'):
            try:
                u,n=text.split('\nNOVA:',1); self.append_chat('YOU',u.replace('USER:','')); self.append_chat('NOVA',n)
            except Exception: self.append_chat('NOVA',text)
        else: self.append_chat('NOVA',text)
if __name__=='__main__': app=QApplication(sys.argv); w=NovaDesktop(); w.show(); sys.exit(app.exec())
