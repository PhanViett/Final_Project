const TrangThaiHoSo = [
  { name: "Hồ Sơ Mới", id: "1" },
  { name: "Hồ Sơ Chờ Thụ Lý", id: "2" },
  { name: "Từ Chối Hồ Sơ", id: "3" },
  { name: "Thụ Lý Hồ Sơ", id: "4" },
  { name: "Yêu Cầu Bổ Sung", id: "5" },
  { name: "Lãnh đạo duyệt yêu cầu bô sung", id: "12" },
  { name: "Chờ Lãnh Đạo Phê Duyệt", id: "6" },
  { name: "Lãnh Đạo Từ Chối", id: "7" },
  { name: "Lãnh Đạo Yêu Cầu Bổ Sung", id: "8" },
  { name: "Đang Trình HĐTV Duyệt", id: "9" },
  { name: "Đang Chờ Cấp Số", id: "10" },
  { name: "Hoàn Thành", id: "11" },
];

const TrangThaiYeuCauLienKet = [
  { label: "Tất cả", id: "" },
  { label: "Yêu cầu mới", id: "1" },
  { label: "Chờ xét duyệt", id: "2" },
  { label: "Đã liên kết", id: "3" },
  { label: "Từ chối liên kết", id: "4" },
];

const GioiTinh = [
  { label: "Nam", value: "1" },
  { label: "Nữ", value: "2" },
  { label: "Giới tính khác", value: "3" },
];

const HinhThuc = [
  { name: "Xét hồ sơ", id: "HT1", label: "Xét hồ sơ", value: "HT1" },
  { name: "Thi thử", id: "HT2", label: "Thi thử", value: "HT2" },
];

const LoaiDeNghi = [
  { name: "Người đề nghị cấp chứng chỉ hành nghề dược lần đầu", id: "LC1" },
  {
    name: "Người đã được cấp chứng chỉ hành nghề dược nhưng chứng chỉ hành nghề dược bị thu hồi theo qui định",
    id: "LC2",
  },
];
const TenChucVu = [
  { label: "PHÓ GIÁM ĐỐC", value: "PHÓ GIÁM ĐỐC" },
  { label: "GIÁM ĐỐC", value: "GIÁM ĐỐC" },
];

const TrangThaiLienKetDuocSi = [
  {
    name: "Tạo mới",
    id: "0",
    color: "primary",
    label: "Tạo mới",
    value: "0",
  },
  {
    name: "Chờ xét duyệt",
    id: "1",
    color: "warning",
    label: "Chờ xét duyệt",
    value: "1",
  },
  {
    name: "Đã liên kết",
    id: "2",
    color: "success",
    label: "Đã liên kết",
    value: "2",
  },
  {
    name: "Từ chối liên kết",
    id: "3",
    color: "danger",
    label: "Từ chối liên kết",
    value: "3",
  },
];

const LoaiMaCCHND = [
  { name: "CCHN-D-SYT-HCM", id: "1", label: "CCHN-D-SYT-HCM", value: "1" },
  { name: "ĐKKDD-HCM", id: "2", label: "ĐKKDD-HCM", value: "2" },
];

const optionsDoiTuong = [
  {
    label: "Giám đốc",
    value: "0",
    id: "Giám đốc",
  },
  {
    label: "Phó giám đốc",
    value: "1",
    id: "Phó giám đốc",
  },
  {
    label: "Trưởng phòng",
    value: "2",
    id: "Trưởng phòng",
  },
  {
    label: "Phó trưởng phòng",
    value: "3",
    id: "Phó trưởng phòng",
  },
  {
    label: "Chuyên viên thụ lý",
    value: "4",
    id: "Chuyên viên thụ lý",
  },
  {
    label: "Chuyên viên hội đồng",
    value: "5",
    id: "Chuyên viên hội đồng",
  },
  {
    label: "Văn thư",
    value: "6",
    id: "Văn thư",
  },
];

export {
  TrangThaiHoSo,
  TrangThaiYeuCauLienKet,
  GioiTinh,
  HinhThuc,
  LoaiDeNghi,
  TrangThaiLienKetDuocSi,
  LoaiMaCCHND,
  TenChucVu,
  optionsDoiTuong,
};
