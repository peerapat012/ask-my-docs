
## Schema

- users
    - uuid auto gen
    - email - uniqe
    - password hash
    - full_name
    - display_name

- docs
    - docs id - uuid auto gen
    - title
    - user_id - fk

- pages
    - pages id - uuid auto gen
    - doc_id - fk
    - page number
    - content - text

อย่างแรก users มีการเก็บ email/password สำหรับการ auth โดยใช้ email/pass
docs มี user_id เก็บเพื่อใช้ บอกว่า docs นี้ของใคร
pages ใช้ doc_id เป๋น fk เพื่อ บอกว่า page นี้ ของ docs อะไร
ส่วน content ใช้ text

## Indexes

- users 
    - uuid เป็น PK กับ email unique post สร้าง Index ให้เอง 
    - query หา email ใช้อยู่แล้ว
    - ตัด (uuid, email) เพราะ uuid เป็น PK หาเจอแถวเดียวอยู่แล้ว ต่อ email ข้างหลังจึงไม่ช่วยอะไร และการหาด้วย email มี UNIQUE index รองรับแล้ว
- docs 
    - เลือก docs.userid เป็น index ส่วน docs.id เป็น PK Auto สร้าง
    - query where โดยใช้ docs.userid
    - ตัด (docs.id, docs.userid) เพราะ Index เรียงตามคอลัมน์แรกก่อน (ในที่นี้คือ id) Postgres จึงกระโดดไปหา userid ใน index นั้นไม่ได้
- pages
    - เลือก (pages.docsid, pages.number) เป็น composite index ส่วน pages.id เป็น pk
    - query ใช้ pages.docsid ใน where เลยต้องให้ pages.docsid อยู่ก่อน pages.numebr ที่ใช้ใน order by
    - ข้อดี docsid ขึ้นก่อน ข้อดีคือไม่ต้อง sort เพิ่ม แต่จะเกิดขึ้นได้ ก็ต่อเมื่อ planner เลือก Index Scan ซึ่งขึ้นกับจำนวนแถวที่ query คืนมาและต้นทุนที่ planner ประเมินไว้ ถ้าเอกสารหนึ่งมีหลายร้อยหน้า planner มีแนวโน้มจะเลือก Index Scan เอง
    - ตัด (pageid, docsid, number) เพราะ Index เรียงตามคอลัมน์แรกก่อน (ในที่นี้คือ id) Postgres จึงกระโดดไปหา docsid ใน index นั้นไม่ได้ เหมือน docs
    - composite ยังไม่เป็น unique เผื่อ content ของหน้านี้เยอะ ต้องแบ่งออก

- sql
    - login: select * from users where email = '';
    - docs: select * from docs where docs.user_id = '';
    - pages: select * from pages where pages.docs_id = '' order by pages.number;

- จำนวนที่รัน
    - users 1,000 rows
    - docs 10,000 rows
    - pages 100,000 rows

- ผลรัน explain analyze
    - users ได้  index scan using uq_users_email
    - docs ได้ bitmap index scan using ix_docs_user_id
    - pages ได้ sort -> bitmap heap scan -> bitmap index scan using ix_pages_doc_id_number แต่ตอนปิด bitmap จะเหลือแค่  index scan using ix_pages_doc_id_number อย่างเดียว โดย อ่านเอกสาร แค่ 10 หน้า

การทำ column datetime ต้องใช้ server_default เพื่อให้ db ใส่ ค่าให้ รวมถึงเวลา migrate กับ rows เก่าด้วย
datetime.utcnow เลิกใช้ เปลี่ยนไปใช้ server_default กับ func.now แทน ซึ่งเป็นฟังค์ชั่นของ postgres
DateTime ต้องใส่ timezone ถ้าไม่ใส่ จะได้ timestamp มาซึงใน db ไม่มี timezone ให้ ต้องเขียน DateTime(timezone = True) ถึงได้ timestamptz