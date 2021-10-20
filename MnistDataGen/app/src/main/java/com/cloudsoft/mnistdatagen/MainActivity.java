package com.cloudsoft.mnistdatagen;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.util.Base64;
import android.util.Log;
import android.util.TypedValue;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    public static final int REQUEST_EXTERNAL_PERMISSION = 12346;
    public static final int type = 1; //1=上传测试数据， 2=上传笔划数据

    private CanvasView canvasView;
    private TextView txtTip;

    private AlertDialog alertDialog; //单选框
    private String curType = "";
    private int curTypeInt = -1;
    private Paint paint;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
//        requestPermissions(this);
        setContentView(R.layout.activity_main);
        canvasView = (CanvasView) findViewById(R.id.canvas_view);
        txtTip = (TextView) findViewById(R.id.txt_tip);
        txtTip.setText("请选择字符类型");

        paint = new Paint();
        paint.setColor(Color.BLACK);
//        paint.setStrokeWidth(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, (float)0.5, getResources().getDisplayMetrics()));
        paint.setStrokeWidth(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, (float)1, getResources().getDisplayMetrics()));
        paint.setStyle(Paint.Style.STROKE);

        StrictMode.ThreadPolicy policy=new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
    }

    public void onMnist(View view){
        String msg = DataUploader.upload3(canvasView.getPointsString());
        if(!msg.equals("")){
            txtTip.setText("识别结果:"+msg);
        }
        return;
    }

    public void onUpload(View view){
        if(curTypeInt == -1 && type != 3){
            txtTip.setText("请先选择数据类型");
            return;
        }
        try {
            if(type == 2){
                DataUploader.upload2(canvasView.getPointsString(), curType);
                return;
            }
            JSONArray points = new JSONArray(canvasView.getPointsString());
            PathObject obj = PathObject.getPathFromAxis(points) ;
            Bitmap bmp = obj.drawPathToSize(paint, 28);

            String b64 = bitmapToBase64(bmp);
            txtTip.setText("正在上传图片请稍候...");
            Boolean res = DataUploader.upload(b64, curTypeInt);
            if(res){
                txtTip.setText("请在画板上写一个 "+curType+" 并上传");
                canvasView.clean();
            }else{
                txtTip.setText("上传失败请稍候再试");
            }
        }catch(Exception err){
            err.printStackTrace();
        }
    }

    public void onClean(View view) {
        canvasView.clean();
    }

    public void showSingleAlertDialog(View view){
        //𠃍, 𠃌
        final String[] items1 = {"0","1","2","3","4","∟","ㄅ","亅","-","6","7","8","9",
                "A","B","C","D","つ","丿","㇏","\uD840\uDCCD","\uD840\uDCCC","乚","乙",
                "√","+","=","×","÷","三","四","五","六","七","九","百","千","万","零","%","<",">",
                "ə", "匹"
        };
        final String[] items2 = {"0","1","2","3","4","5","6","7","8","9",
                "+","-","×","÷","=",">","<",".","(",
                ")","%","[","]","A","B","C","D","E","F","G","√",
                "个","百","千","万","三","四","五","六","七","八","九","零",
                "①","②","③","④","a","b","d","e","f","≠","≈"
        };

        AlertDialog.Builder alertBuilder = new AlertDialog.Builder(this);
        alertBuilder.setTitle("选择手写数据");
        if(type == 2){
            alertBuilder.setSingleChoiceItems(items1, 0, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {
//                Toast.makeText(MainActivity.this, items[i], Toast.LENGTH_SHORT).show();
                    curType = items1[i];
                    curTypeInt = i;
                    txtTip.setText("请在画板上写一个 "+curType+" 并上传");
                }
            });
        }else{
            alertBuilder.setSingleChoiceItems(items1, 0, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialogInterface, int i) {
//                Toast.makeText(MainActivity.this, items[i], Toast.LENGTH_SHORT).show();
                    curType = items1[i];
                    curTypeInt = i;
                    txtTip.setText("请在画板上写一个 "+curType+" 并上传");
                }
            });
        }


        alertBuilder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                alertDialog.dismiss();
            }
        });

        alertBuilder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                alertDialog.dismiss();
            }
        });

        alertDialog = alertBuilder.create();
        alertDialog.show();
    }

    public static boolean requestPermissions(Activity activity) {
        Log.i("mnist", "读写储存权限 ："+(ContextCompat.checkSelfPermission(activity, android.Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED));
        Log.i("mnist", "启动相机权限 ："+(ContextCompat.checkSelfPermission(activity, android.Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED));
        Log.i("mnist", "读取手机状态权限 ："+(ContextCompat.checkSelfPermission(activity, android.Manifest.permission.READ_PHONE_STATE) == PackageManager.PERMISSION_GRANTED));
        if (ContextCompat.checkSelfPermission(activity, android.Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
                ||ContextCompat.checkSelfPermission(activity, android.Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED
                ||ContextCompat.checkSelfPermission(activity, android.Manifest.permission.READ_PHONE_STATE) != PackageManager.PERMISSION_GRANTED
        ) {
            Log.e("CameraActivity.java.hx:", "尝试获取储存以及相机权限");
            //请求权限
            if (ActivityCompat.shouldShowRequestPermissionRationale(activity, android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    || ActivityCompat.shouldShowRequestPermissionRationale(activity, android.Manifest.permission.CAMERA)
                    || ActivityCompat.shouldShowRequestPermissionRationale(activity, android.Manifest.permission.READ_PHONE_STATE)
            ) {
//                showToast("请开启 储存权限。", activity);
                ActivityCompat.requestPermissions(activity, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE,android.Manifest.permission.CAMERA,android.Manifest.permission.READ_PHONE_STATE,android.Manifest.permission.ACCESS_FINE_LOCATION}, REQUEST_EXTERNAL_PERMISSION);
                return false;
            }else{
//                showToast("请开启 储存权限。", activity);
                ActivityCompat.requestPermissions(activity, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE,android.Manifest.permission.CAMERA,android.Manifest.permission.READ_PHONE_STATE,android.Manifest.permission.ACCESS_FINE_LOCATION}, REQUEST_EXTERNAL_PERMISSION);
                return true;
            }
        }
        return true;
    }

    /**
     * bitmap转为base64
     *
     * @param bitmap
     * @return
     */
    public static String bitmapToBase64(Bitmap bitmap) {
        String result = null;
        ByteArrayOutputStream baos = null;
        try {
            if (bitmap != null) {
                baos = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
                baos.flush();
                baos.close();
                byte[] bitmapBytes = baos.toByteArray();
                result = Base64.encodeToString(bitmapBytes, Base64.DEFAULT);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (baos != null) {
                    baos.flush();
                    baos.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
//        Log.i("mnist:", result);
        return result;
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        if (event.getKeyCode() == KeyEvent.KEYCODE_BACK ) {
            return true;
        } else {
            return super.dispatchKeyEvent(event);
        }
    }
}
