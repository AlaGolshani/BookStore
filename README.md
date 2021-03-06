<div dir="rtl">
<h1>کتاب فروشی</h1>

این پروژه یک سایت کتاب فروشی به شرح زیر می باشد.

![Screenshot 2021-09-02 203622](https://user-images.githubusercontent.com/74684218/131879460-45a2ed77-38a8-4695-ac42-5079ed8b2a73.jpg)

سه نوع کاربر مدیر، کارمند و مشتری وجود دارد که هر کدام دسترسی ها، امکانات و پنل های خود را دارند.

امکانات مشتریان:
- اضافه کردن کتاب به سبد خرید خود
- اعمال کردن تخفیف روی سبد خرید (درصورت داشتن کد تخفیف)
- انتخاب آدرسی که سفارش باید به آن ارسال شود و ثبت نهایی سفارش
- مشاهده تاریخچه سفارشات
- مشاهده و ویرایش پروفایل
- اضافه کردن، ویرایش و حذف آدرس های خود
- ...

![Screenshot 2021-09-02 200125](https://user-images.githubusercontent.com/74684218/131879857-e0fa267b-4359-4873-8724-e6c52a3da12e.jpg)
![Screenshot 2021-09-02 205935](https://user-images.githubusercontent.com/74684218/131882075-f95368f9-764a-4129-a0d1-7c2801ef4c44.jpg)

امکانات کارمندان:
- اضافه کردن، ویرایش یا حذف کتاب ها
- اضافه کردن، ویرایش یا حذف دسته بندی های کتاب ها
- اضافه کردن، ویرایش یا حذف تخفیف ها
- ...

امکانات مدیران:
- مدیران تمامی دسترسی های کارمندان را دارند
- علاوه بر آن در پنل خود یک بخش گزارشگیری داشته که شامل گزارش های زیر است:
	- تعداد مشتریان، کارمندان، مدیران
	- درامد کلی سایت
	- تعداد کل سفارشات
	- تعداد محصولات تخفیف دار و بدون تخفیف

![Screenshot 2021-09-02 194209](https://user-images.githubusercontent.com/74684218/131869617-53651b83-d573-4a37-9d5e-853dc6ddb58a.jpg)

- قابلیت سرچ بر اساس نام کتاب یا نویسنده برای تمامی کاربران فعال است.

انواع تخفیف ها:
- نقدی (کارمند یا مدیر روی کتاب ها تعریف می کنند)
- درصدی (کارمند یا مدیر روی کتاب ها تعریف می کنند)
- کد تخفیف (کارمند یا مدیر آن را تعریف می کنند و مشتری می تواند هنگام نهایی کردن سفارش خود از آن استفاده کند)

سایر توضیحات:
- برای مدیریت اکانت ها، authentication و registration از پکیج allauth استفاده شده است.
- دیتابیس: postgreSQL

</div>
