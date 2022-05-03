# coding=utf-8
import builtins

import numpy as np
import pytest

from da_datafix.files import from_csv


class co2_mocker:
    dat = [
        "timestamp,139_value,140_value,137_value,202_value,242_value,237_value,234_value,239_value,236_value,235_value,205_value,240_value,337_value,347_value,334_value,364_value,344_value,341_value,361_value,369_value,346_value,363_value,335_value,340_value,370_value,336_value,333_value,365_value,342_value,339_value,371_value,366_value,343_value,465_value,442_value,432_value,438_value,434_value,461_value,433_value,439_value,466_value,471_value,443_value,463_value,440_value,470_value,436_value,464_value,536_value,542_value,532_value,543_value,537_value,541_value,535_value,534_value",
        "01-Mar-22 12:00:00 AM EET,397.00,391.00,471.00,583.00,378.00,335.00,438.00,428.00,397.00,490.00,464.00,412.00,430.00,432.00,322.00,385.00,419.00,443.00,425.00,420.00,426.00,471.00,452.00,485.00,439.00,442.00,387.00,465.00,430.00,468.00,469.00,365.00,390.00,462.00,404.00,388.00,412.00,370.00,421.00,238.00,334.00,394.00,398.00,390.00,431.00,602.00,425.00,370.00,415.00,387.00,429.00,458.00,430.00,495.00,509.00,469.00,492.00",
        "01-Mar-22 12:05:00 AM EET,371.00,398.00,468.00,587.00,382.00,343.00,425.00,438.00,400.00,496.00,463.00,410.00,426.00,426.00,327.00,383.00,408.00,443.00,417.00,426.00,423.00,472.00,445.00,482.00,437.00,451.00,377.00,466.00,415.00,460.00,458.00,361.00,403.00,457.00,404.00,394.00,410.00,363.00,419.00,231.00,336.00,394.00,390.00,394.00,432.00,597.00,441.00,363.00,418.00,396.00,437.00,458.00,427.00,499.00,516.00,465.00,495.00",
        "01-Mar-22 12:10:00 AM EET,387.00,395.00,469.00,588.00,393.00,340.00,435.00,439.00,401.00,490.00,460.00,408.00,437.00,430.00,328.00,383.00,412.00,444.00,422.00,433.00,426.00,467.00,441.00,482.00,440.00,442.00,388.00,466.00,420.00,467.00,461.00,369.00,392.00,460.00,402.00,388.00,414.00,360.00,415.00,234.00,327.00,397.00,401.00,396.00,433.00,598.00,437.00,360.00,414.00,406.00,425.00,467.00,429.00,500.00,506.00,458.00,497.00",
        "01-Mar-22 12:15:00 AM EET,383.00,401.00,467.00,581.00,371.00,342.00,432.00,428.00,395.00,487.00,452.00,410.00,432.00,429.00,315.00,378.00,402.00,448.00,428.00,428.00,427.00,463.00,435.00,479.00,445.00,445.00,372.00,467.00,417.00,467.00,461.00,370.00,399.00,452.00,396.00,388.00,407.00,356.00,426.00,232.00,338.00,395.00,397.00,398.00,439.00,598.00,435.00,356.00,414.00,397.00,433.00,472.00,435.00,508.00,510.00,470.00,493.00",
        "01-Mar-22 12:20:00 AM EET,355.00,399.00,469.00,578.00,379.00,344.00,435.00,441.00,404.00,490.00,460.00,410.00,427.00,426.00,318.00,370.00,416.00,449.00,422.00,423.00,428.00,468.00,451.00,480.00,448.00,445.00,377.00,459.00,420.00,462.00,461.00,370.00,389.00,454.00,400.00,394.00,407.00,373.00,425.00,233.00,332.00,399.00,400.00,391.00,435.00,597.00,432.00,373.00,418.00,390.00,432.00,469.00,429.00,503.00,511.00,457.00,493.00",
        "01-Mar-22 12:25:00 AM EET,372.00,414.00,475.00,577.00,376.00,344.00,440.00,431.00,399.00,494.00,460.00,410.00,435.00,436.00,320.00,371.00,409.00,448.00,420.00,423.00,426.00,480.00,449.00,475.00,442.00,448.00,373.00,459.00,420.00,459.00,460.00,361.00,402.00,460.00,401.00,394.00,408.00,362.00,408.00,221.00,326.00,403.00,398.00,388.00,439.00,590.00,430.00,362.00,414.00,401.00,436.00,457.00,425.00,505.00,513.00,458.00,488.00",
        "01-Mar-22 12:30:00 AM EET,371.00,392.00,465.00,575.00,372.00,341.00,437.00,428.00,401.00,492.00,463.00,407.00,428.00,430.00,315.00,370.00,412.00,447.00,423.00,424.00,427.00,474.00,439.00,485.00,443.00,447.00,382.00,457.00,425.00,461.00,457.00,363.00,393.00,465.00,401.00,405.00,412.00,369.00,411.00,230.00,335.00,399.00,401.00,395.00,436.00,607.00,431.00,369.00,409.00,396.00,428.00,468.00,425.00,497.00,502.00,461.00,490.00",
        "01-Mar-22 12:35:00 AM EET,357.00,401.00,462.00,571.00,379.00,340.00,440.00,426.00,402.00,487.00,469.00,410.00,432.00,437.00,321.00,382.00,402.00,446.00,430.00,421.00,426.00,468.00,447.00,477.00,442.00,448.00,385.00,461.00,416.00,457.00,461.00,360.00,395.00,453.00,395.00,398.00,412.00,365.00,422.00,239.00,334.00,404.00,403.00,393.00,436.00,596.00,436.00,365.00,417.00,391.00,434.00,453.00,435.00,498.00,508.00,462.00,494.00",
    ]

    def __enter__(self, *args, **kwargs):
        return self.dat

    def __exit__(self, *args, **kwargs):
        pass



@pytest.fixture
def mocked_co2_file(monkeypatch):
    monkeypatch.setattr(builtins, "open", lambda x: co2_mocker())


def test_city(mocked_co2_file):
    model = from_csv("MOCKED FILENAME")
    data = model.get_data_np()
    assert data.shape == (8,)
    assert data["440_value"][0] == 602.0
    assert data["205_value"][1] == 463.0
    assert data["timestamp"][0] == np.datetime64("2022-03-01T00:00:00")
    assert data["timestamp"][7] == np.datetime64("2022-03-01T00:35:00")


