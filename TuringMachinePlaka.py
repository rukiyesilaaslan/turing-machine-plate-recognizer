import sys

class TuringMachineSimulator:
    def __init__(self, input_string):
        # Ödev kurallarına göre bant yapısını kuruyoruz.
        # Girdinin sonuna Turing Makinesi bitişini simüle etmek için Boşluk (B) ekliyoruz.
        self.tape = list(input_string) + ['#']
        self.head_position = 0
        self.current_state = 'q0'
        
        # Geçiş Fonksiyonu Tanımı: (mevcut_durum, okunan_karakter_türü) -> (yeni_durum, yön)
        # Karakter türleri: 'N' (Rakam), 'L' (Büyük Harf), 'B' (Boşluk)
        self.transitions = {
            'q0': {'N': ('q1', 'R')},
            'q1': {'N': ('q2', 'R')},
            'q2': {'L': ('q3', 'R')},
            'q3': {'L': ('q4', 'R')},
            'q4': {'N': ('q5', 'R')},
            'q5': {'N': ('q6', 'R')},
            'q6': {'N': ('q7', 'R')},
            'q7': {'#': ('q_accept', 'S')}
        }

    def _get_char_type(self, char):
        if char == '#':
            return '#'
        elif char.isdigit():
            return 'N'
        elif char.isalpha() and char.isupper():
            return 'L'
        else:
            return 'INVALID'  # Küçük harfler veya özel semboller doğrudan RED'e düşer

    def print_step(self, step, char):
        # Bandın ve okuma kafasının anlık konumunu görselleştirir
        tape_str = "".join(self.tape)
        visual_pointer = [' '] * len(tape_str)
        visual_pointer[self.head_position] = '^'
        pointer_str = "".join(visual_pointer)
        
        print(f"Adım {step}:")
        print(f"  Mevcut Durum   : {self.current_state}")
        print(f"  Okunan Sembol  : {char}")
        print(f"  Bant İçeriği   : {tape_str}")
        print(f"  Kafa Konumu    : {pointer_str}")
        print("-" * 45)

    def run(self):
        step = 1
        print(f"\nSimülasyon Başlıyor... Girdi: {''.join(self.tape[:-1])}")
        print("=" * 45)
        
        while self.current_state not in ['q_accept', 'q_reject']:
            # Kafa sınır kontrolü
            if self.head_position < 0 or self.head_position >= len(self.tape):
                self.current_state = 'q_reject'
                break
                
            current_char = self.tape[self.head_position]
            char_type = self._get_char_type(current_char)
            
            self.print_step(step, current_char)
            step += 1
            
            # Durum geçiş kontrolü
            state_transitions = self.transitions.get(self.current_state, {})
            if char_type in state_transitions:
                next_state, direction = state_transitions[char_type]
                self.current_state = next_state
                
                # Kafayı kurallara göre hareket ettir
                if direction == 'R':
                    self.head_position += 1
                elif direction == 'L':
                    self.head_position -= 1
                # 'S' (Stationary/Sabit) durumunda kafa yerinde kalır
            else:
                # Tanımlanmamış geçiş durumu -> Doğrudan RED (Kritik Gereksinim 5,6,7,8,9)
                self.current_state = 'q_reject'
        
        # Nihai Karar Çıktısı
        if self.current_state == 'q_accept':
            print("SONUÇ: KABUL\n")
            return "KABUL"
        else:
            print("SONUÇ: RED\n")
            return "RED"

if __name__ == "__main__":
    # Konsoldan etkileşimli çalıştırma
    if len(sys.argv) > 1:
        plaka = sys.argv[1]
        tm = TuringMachineSimulator(plaka)
        tm.run()
    else:
        user_input = input("Lütfen test etmek istediğiniz plaka girdisini yazın: ")
        tm = TuringMachineSimulator(user_input)
        tm.run()