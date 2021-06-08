from data_merge import employee_skill

# 그룹핑한 데이터프레임 가져옴

# 직원 번호로 그룹핑
em_skill_df = employee_skill()

# 레고 기수만 뽑아봄 (21년 입사)
LEGO_NUMS = em_skill_df[em_skill_df['JIKWON_NO'] > 21000000]['JIKWON_NO'].unique()
print(LEGO_NUMS)
grouped_employee_skill = em_skill_df.groupby(['JIKWON_NO'])

for lego_no in LEGO_NUMS:
    one_employee_skill = grouped_employee_skill.get_group(lego_no)
    print(one_employee_skill)
    print(lego_no, one_employee_skill.size)

print("===============================================================================")


def one_emp_skill(emp_no):
    one_emp_info = grouped_employee_skill.get_group(emp_no)

    # 우선 파일명 (COL05)을 보고 확장자가 있는지 봄 -> 세부 카테고리
    one_emp_info['extension'] = one_emp_info['COL05'].str.split(".").str[1]

    # 프로그램 종류 (COL04)을 보고 필터링 해주기
    one_emp_info.drop(['COL05'], axis=1, inplace=True)
    print(one_emp_info)


one_emp_skill(21100284)
