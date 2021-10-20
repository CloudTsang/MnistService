package com.cloudsoft.mnistdatagen;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Point;
import android.graphics.Rect;
import android.os.Environment;
import android.util.AttributeSet;
import android.util.Log;
import android.util.TypedValue;
import android.view.MotionEvent;
import android.view.View;

import org.json.JSONArray;

import java.io.File;
import java.io.FileOutputStream;

/**
 * @author zijiao
 * @version 17/8/2
 */
public class CanvasView extends View {

    public Paint paint;
    private Path path;
    private final int spec;
    private String points = "[";

    public CanvasView(Context context) {
        this(context, null);
    }

    public CanvasView(Context context, AttributeSet attrs) {
        super(context, attrs);

        paint = new Paint();
        paint.setColor(Color.BLACK);
        paint.setStrokeWidth(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 3, getResources().getDisplayMetrics()));
        paint.setStyle(Paint.Style.STROKE);

        path = new Path();
        int screenWidth = getResources().getDisplayMetrics().widthPixels;
        spec = MeasureSpec.makeMeasureSpec(screenWidth, MeasureSpec.EXACTLY);
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        // 画板宽高写死为屏幕宽度
        super.onMeasure(spec, spec);
//        super.onMeasure(widthMeasureSpec,heightMeasureSpec);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawPath(path, paint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int x = (int)event.getX();
        int y = (int)event.getY();
        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                if (points.contains("]]]")) {
                    points.replace("]]]", "]],");
                }
                path = new Path(path);
                path.moveTo(x, y);
                points += "[[" + (int) x + "," + (int) y + "]";
                break;
            case MotionEvent.ACTION_MOVE:
                path.lineTo(x, y);
                points += ",[" + (int) x + "," + (int) y + "]";
                break;
            case MotionEvent.ACTION_UP:
                points += "],";
                break;
        }

        invalidate();
        return true;
    }

    public String getPointsString(){
        if(points.length() == 1){
            return "[]";
        }
        String retPoints = points.substring(0, points.length() - 1);
        retPoints = retPoints + "]";
        return retPoints;
    }

    public void clean() {
        path.reset();
        points = "[";
        invalidate();
    }

    public boolean isEmpty() {
        return path.isEmpty();
    }

    public Bitmap getCanvasBmp(){
        try{
            setDrawingCacheEnabled(true);
            setDrawingCacheQuality(View.DRAWING_CACHE_QUALITY_LOW);
            Bitmap cache = getDrawingCache();
            return cache;
        }catch (Exception err){
            err.printStackTrace();
        }
        return null;
    }


    public static void fillInputData(Bitmap bm, float[] data, int newWidth, int newHeight) {
        // 获得图片的宽高
        int width = bm.getWidth();
        int height = bm.getHeight();
        // 计算缩放比例
        float scaleWidth = ((float) newWidth) / width;
        float scaleHeight = ((float) newHeight) / height;
        // 取得想要缩放的matrix参数
        Matrix matrix = new Matrix();
        matrix.postScale(scaleWidth, scaleHeight);
        // 得到新的图片
        Bitmap newbm = Bitmap.createBitmap(bm, 0, 0, width, height, matrix, true);
        for (int y = 0; y < newHeight; y++) {
            for (int x = 0; x < newWidth; x++) {
                int pixel = newbm.getPixel(x, y);
              //  Log.i("mnist:" , "pixel = "+pixel);
                data[newWidth * y + x] = pixel == 0xffffffff ? 0 : 1;
            }
        }
    }

    private Bitmap resizeBitmap(Bitmap bm, int newWidth, int newHeight) {
        // 获得图片的宽高
        int width = bm.getWidth();
        int height = bm.getHeight();
        // 计算缩放比例
        float scaleWidth = ((float) newWidth) / width;
        float scaleHeight = ((float) newHeight) / height;
        // 取得想要缩放的matrix参数
        Matrix matrix = new Matrix();
        matrix.postScale(scaleWidth, scaleHeight);
        // 得到新的图片
        Bitmap newbm = Bitmap.createBitmap(bm, 0, 0, width, height, matrix, true);
        return newbm;
    }


    private void savePicture(Bitmap bmp, String path){
        try{
            File extDir = Environment.getExternalStorageDirectory();
            File file = new File(extDir, path);
            if(file.exists()){
                file.delete();
            }
            FileOutputStream out;
            out = new FileOutputStream(file);
            if(bmp.compress(Bitmap.CompressFormat.JPEG, 100, out))
            {
                out.flush();
                out.close();
            }
        }catch(Exception err){
            err.printStackTrace();
        }
    }
}
