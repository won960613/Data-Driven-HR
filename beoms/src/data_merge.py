# data merge and preprocessing
import os
import pandas as pd


def init():
    # 열 전체 보기
    pd.set_option('display.max_columns', None)

    dataPath = os.path.join(os.getcwd(), '../data')

    # 윈도우 환경에서 엑셀 열고 닫으면 인코딩 형식 cp949
    employee = pd.read_csv(os.path.join(dataPath, './employee.csv'), encoding='cp949')
    project_info = pd.read_csv(os.path.join(dataPath, './project_info.csv'), encoding='cp949')
    project_people = pd.read_csv(os.path.join(dataPath, './project_people.csv'), encoding='cp949')
    program_history1 = pd.read_csv(os.path.join(dataPath, './program_history1.csv'), encoding='cp949')
    program_history2 = pd.read_csv(os.path.join(dataPath, './program_history2.csv'), encoding='cp949')
    program_history = pd.concat([program_history1, program_history2], ignore_index=True)

    # drop column idx
    employee_drop_columns_idx = [3, 7, 8, 11, 14, 18, 20, 21, 22, 23]
    project_info_drop_columns_idx = [0, 1, 2, 4, 7]
    project_info_drop_columns_idx.extend(list(range(16, len(project_info.columns))))
    program_history_drop_columns_idx = [5, 12]

    employee_drop_columns = [employee.columns[idx] for idx in employee_drop_columns_idx]
    project_info_drop_columns = [project_info.columns[idx] for idx in project_info_drop_columns_idx]
    program_history_drop_columns = [program_history.columns[idx] for idx in program_history_drop_columns_idx]

    employee.drop(employee_drop_columns, axis=1, inplace=True)
    project_info.drop(project_info_drop_columns, axis=1, inplace=True)
    program_history.drop(program_history_drop_columns, axis=1, inplace=True)

    # ICT 직원들만 뽑음
    is_ict_employee = (employee['JEOM_NO'] == 61) | (employee['JEOM_NO'] == 62) | (employee['JEOM_NO'] == 63) \
                      | (employee['JEOM_NO'] == 64) | (employee['JEOM_NO'] == 66) | (employee['JEOM_NO'] == 69) | (
                                  employee['JEOM_NO'] == 507)
    ict_employee = employee[is_ict_employee]

    # BK 수정
    program_history = program_history[program_history['COL07'].str[:2] == 'BK']
    program_history['COL07'] = program_history['COL07'].str[2:].astype(int)

    # 직원 df와 프로그램 이력 df join
    merged_employee_program = pd.merge(ict_employee, program_history, left_on='JIKWON_NO', right_on='COL07',
                                       how='outer')
    # print(merged_employee_program.columns)

    # 프로그램 형식명만 보기 위해 직군과 연결 - COL04: 프로그램 종류 / COL05: 프로그램 이름
    raw_employee_skill = merged_employee_program[['JIKWON_NO', 'NAME', 'COL04', 'COL05']]

    # Nan 있는 행 제거
    refined_employee_skill = raw_employee_skill.dropna(axis=0)

    return refined_employee_skill


def employee_skill():
    return init()
