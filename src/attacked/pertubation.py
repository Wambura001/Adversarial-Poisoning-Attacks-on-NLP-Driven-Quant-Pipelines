import random
import re

class KoreanFinBERTPoisoner:
    """
    An adversarial ML script designed to poison financial sentiment pipelines.
    Target Pipeline: FinBERT (Sentiment Processing) + LSTM (Quantitative Execution)
    """
    def __init__(self):
        # Dictionary of structural Korean financial keywords mapped to high-frequency retail slang
        # Designed to mislead FinBERT tokenization while remaining perfectly legible to humans.
        self.slang_substitution_matrix = {
            "급등": ["떡상", "폭등빔", "개급등"],
            "폭락": ["떡락", "참혹한 폭락", "한강진입"],
            "매수": ["풀매수", "영끌매수", "줍줍"],
            "매도": ["빤스런", "손절탈출", "던지기"],
            "호재": ["킹재", "씹호재", "초대형 호재"],
            "악재": ["대악재", "지옥행 악재", "악재악재"],
            "수익": ["익절", "수익인증", "달달한수익"],
            "손실": ["물림", "반토막", "구조대요망"]
        }
        
        # Zero-Width / Invisible Unicode characters used to break BERT WordPiece tokenizers
        self.invisible_breaker = "\u200b"

    def apply_semantic_slang(self, text: str, attack_probability: float = 0.5) -> str:
        """
        Replaces standard Korean financial terms with hyper-targeted forum slang.
        """
        words = text.split()
        for i, word in enumerate(words):
            for target_keyword, slang_options in self.slang_substitution_matrix.items():
                if target_keyword in word and random.random() < attack_probability:
                    chosen_slang = random.choice(slang_options)
                    # Replace the specific root keyword inside the word string
                    words[i] = word.replace(target_keyword, chosen_slang)
        return " ".join(words)

    def inject_token_breakers(self, text: str, attack_probability: float = 0.3) -> str:
        """
        Injects zero-width space characters directly inside critical words.
        This forces FinBERT's tokenizer to split unified concepts into Unknown [UNK] 
        or out-of-context subwords, blinding the downstream LSTM model to key market trends.
        """
        words = text.split()
        for i, word in enumerate(words):
            if len(word) > 2 and random.random() < attack_probability:
                # Inject an invisible breaker character directly in the middle of the string
                midpoint = len(word) // 2
                words[i] = word[:midpoint] + self.invisible_breaker + word[midpoint:]
        return " ".join(words)

    def generate_adversarial_headline(self, clean_text: str) -> str:
        """
        Executes the dual-stage adversarial text formatting pipeline.
        """
        # Step 1: Shift syntax towards unstructured retail slang
        poisoned_text = self.apply_semantic_slang(clean_text, attack_probability=0.8)
        # Step 2: Inject character-level tokenization exploits
        poisoned_text = self.inject_token_breakers(poisoned_text, attack_probability=0.4)
        return poisoned_text

# --- Verification & Simulation Run ---
if __name__ == "__main__":
    print("=" * 70)
    print("SIMULATING KOREAN MARKET SENTIMENT POISONING ATTACK ENGINE")
    print("=" * 70)
    
    # Mock data mirroring Korean financial forum pipelines (Naver Financial / Paxnet)
    sample_clean_headlines = [
        "삼성전자 반도체 공급 계약 호재로 인해 주가 급등 예상",
        "금리 인상 조치 발표에 따른 기관 투자자 대규모 매도세 집계",
        "에코프로 신규 공장 가공 소식 발표 이후 개인 투자자 풀매수 지속",
        "실적 악화 공시 발표로 인한 장외 거래 시장 폭락 우려 심화"
    ]
    
    poisoner = KoreanFinBERTPoisoner()
    
    for idx, clean_headline in enumerate(sample_clean_headlines, start=1):
        poisoned_headline = poisoner.generate_adversarial_headline(clean_headline)
        
        print(f"\n[Scenario #{idx}]")
        print(f" Clean Data Input  : {clean_headline}")
        print(f" Poisoned Adversarial Output: {poisoned_headline}")
        
    print("\n" + "=" * 70)
    print("Execution complete. Ready for injection testing into FinBERT + LSTM pipeline.")
    print("=" * 70)
