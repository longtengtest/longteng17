import pytest
import pytest_check as ck



@pytest.mark.p1
@pytest.mark.api
def test_add_fuel_card_normal(base_url,db, data, api):
    print(data)
    url = base_url+'/gasStation/process'
    data_source_id = data.get('data_source_id')
    card_number = data.get('card_number')

    # # 环境检查
    # card = db.query(f"SELECT id FROM cardinfo WHERE cardNumber={card_number}")
    # if card:
    #     pytest.skip("卡号已存在")
    # 环境准备
    db.change_db(f"DELETE FROM cardinfo WHERE cardNumber={card_number}")
    json_data = {
        "dataSourceId": data_source_id,
        "methodId": "00A",
        "CardInfo": {
            "cardNumber": card_number
        }
    }
    res = api.post(url, json=json_data)
    # print(res)
    res_dict = res.json()
    ck.equal(200,res_dict.get("code"))
    ck.equal("添加卡成功",res_dict.get("msg"))
    ck.is_true()
