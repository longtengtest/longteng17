import pytest
import pytest_check as ck


@pytest.mark.p1
@pytest.mark.api
def test_add_fuel_card_normal(api, db, case_data):
    """正常添加加油卡"""
    url = '/gasStation/process'
    data_source_id = case_data.get('data_source_id')
    card_number = case_data.get('card_number')

    # 环境检查
    if db.check_card(card_number):
        pytest.skip(f'卡号: {card_number} 已存在')

    json_data = {"dataSourceId": data_source_id, "methodId": "00A",
                 "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    ck.equal(200, res_dict.get("code"))
    ck.equal("添加卡成功", res_dict.get("msg"))
    ck.is_false(res_dict.get('success'))
    # 数据库断言
    ck.is_true(db.check_card(card_number))

    # 环境清理
    db.del_card(card_number)

