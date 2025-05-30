# evaluation.py

from sklearn.metrics import precision_score, recall_score, f1_score
import re

def normalize_cve_ids(cve_list):
    """
    CVE ID 리스트를 대문자로 통일하고 정규 표현식으로 정리
    """
    normalized = []
    for cve in cve_list:
        match = re.search(r'CVE-\d{4}-\d{4,7}', cve.upper())
        if match:
            normalized.append(match.group())
    return list(set(normalized))  # 중복 제거


def evaluate_cve_id_extraction(predicted_ids, ground_truth_ids):
    """
    CVE ID 추출 성능을 Precision, Recall, F1로 평가
    - predicted_ids: 모델이 예측한 CVE ID 리스트
    - ground_truth_ids: 사용자가 입력한 정답 CVE ID 리스트
    """
    y_true = []
    y_pred = []

    # 정규화
    predicted = normalize_cve_ids(predicted_ids)
    ground_truth = normalize_cve_ids(ground_truth_ids)

    # 각 고유한 CVE ID 기준으로 비교
    all_ids = set(predicted + ground_truth)
    for cve_id in all_ids:
        y_true.append(int(cve_id in ground_truth))
        y_pred.append(int(cve_id in predicted))

    # 스코어 계산
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return precision, recall, f1
