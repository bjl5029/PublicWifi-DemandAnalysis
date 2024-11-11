각 지역별 csv 파일을 생성한 뒤, 30분(api 갱신이 30분마다임)마다 api 호출하여 reponse를 필터링하고 csv에 갱신해서 저장함.
(필터링되어 삭제된 response의 값들은 null값임. 검토 필요 X)
