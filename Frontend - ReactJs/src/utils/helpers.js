import moment from "moment";
import { toast } from "react-toastify";

const ChangeToSlug = (title) => {
  var slug;
  slug = title.toLowerCase();

  //Đổi ký tự có dấu thành không dấu
  slug = slug.replace(/á|à|ả|ạ|ã|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ/gi, "a");
  slug = slug.replace(/é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ/gi, "e");
  slug = slug.replace(/i|í|ì|ỉ|ĩ|ị/gi, "i");
  slug = slug.replace(/ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ/gi, "o");
  slug = slug.replace(/ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự/gi, "u");
  slug = slug.replace(/ý|ỳ|ỷ|ỹ|ỵ/gi, "y");
  slug = slug.replace(/đ/gi, "d");
  //Xóa các ký tự đặt biệt
  slug = slug.replace(
    /\`|\~|\!|\@|\#|\||\$|\%|\^|\&|\*|\(|\)|\+|\=|\,|\.|\/|\?|\>|\<|\'|\"|\:|\;|_/gi,
    ""
  );
  //Đổi khoảng trắng thành ký tự gạch ngang
  slug = slug.replace(/ /gi, "-");
  //Đổi nhiều ký tự gạch ngang liên tiếp thành 1 ký tự gạch ngang
  //Phòng trường hợp người nhập vào quá nhiều ký tự trắng
  slug = slug.replace(/\-\-\-\-\-/gi, "-");
  slug = slug.replace(/\-\-\-\-/gi, "-");
  slug = slug.replace(/\-\-\-/gi, "-");
  slug = slug.replace(/\-\-/gi, "-");
  //Xóa các ký tự gạch ngang ở đầu và cuối
  slug = "@" + slug + "@";
  slug = slug.replace(/\@\-|\-\@|\@/gi, "");
  return slug;
};

const changeTime = (date, type) => {
  switch (type) {
    case "d/m/y":
      return moment(date).format("DD/MM/yyyy");
    case "d/m/y h:m":
      return moment(date).format("DD/MM/yyyy HH:mm");
    default:
      return moment(date).format("DD/MM/yyyy");
  }
};


const take_decimal_number = (num, n) => {
  //num : số cần xử lý
  //n: số chữ số sau dấu phẩy cần lấy
  let base = 10 ** n;
  let result = Math.round(num * base) / base;
  return result;
}

const formatNumber = (number) => {
  var temp = String(number);
  temp = temp.replace(/\D/g, "");
  if (temp === "0") {
    return "0";
  }
  var result = temp;
  if (temp.length > 3) {
    var result = "";
    for (var i = temp.length - 1, count = 1; i >= 0; --i, ++count) {
      result = temp[i] + result;
      if (count % 3 === 0 && i !== 0) {
        result = "." + result;
      }
    }
  }
  return result;
};

const checkNoti = (type = "warning", text = "Bạn không có quyền thực hiện thao tác này") => {
  switch (type) {
    case "warning":
      toast.warning(text, {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        toastId: "success",
      })
      break;
    case "success":
      toast.success(text, {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        toastId: "success",
      })
      break;
    case "danger":
      toast.danger(text, {
        position: "top-right",
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        toastId: "success",
      })
      break;
    default:
      break;
  }
}




export { ChangeToSlug, changeTime, formatNumber, take_decimal_number, checkNoti };
