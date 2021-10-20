package com.cloudsoft.mnistdatagen;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;

import android.os.StrictMode;
import android.util.Log;
import org.json.JSONArray;

import java.util.ArrayList;
import java.util.List;

public class PathObject {
    public List<Path> paths;
    public List<JSONArray> points;
    public int maxX = -1;
    public int maxY = -1;
    public int minX = -1;
    public int minY = -1;
    public PathObject(){
            paths = new ArrayList<>();
            points = new ArrayList<>();
    }

    public boolean addPaths(PathObject obj){
        if(paths.size()>=2){
            return false;
        }
        paths.addAll(obj.paths);
        minX = (minX==-1)?obj.minX:Math.min(obj.minX,minX);
        minY = (minY==-1)?obj.minY:Math.min(obj.minY,minY);
        maxX = (maxX==-1)?obj.maxX:Math.max(obj.maxX,maxX);
        maxY = (maxY==-1)?obj.maxY:Math.max(obj.maxY,maxY);
        points.addAll(obj.points);
        return true;
    }

    public Bitmap drawPathToSize(Paint paint, int psize){
        Bitmap b = Bitmap.createBitmap(psize, psize, Bitmap.Config.ARGB_8888);
        b.eraseColor(Color.parseColor("#FFFFFF"));
        Canvas c = new Canvas(b);

        float scaleWidth = (float) (psize * 0.9) / (maxX - minX);
        float scaleHeight = (float) (psize * 0.9) / (maxY - minY);
        float scale = Math.min(scaleHeight, scaleWidth);
        Matrix matrix = new Matrix();
        matrix.setScale(scale,scale);

        float offsetX = (psize - (maxX-minX)*scale)/2;
        float offsetY = (psize - (maxY-minY)*scale)/2;
        float startX = minX*scale;
        float startY = minY*scale;
//        Log.i("mnist", "paths.size()=" + paths.size());
        for(int i=0; i<paths.size(); i++){
            Path p = new Path(paths.get(i));
            p.transform(matrix);
            p.offset(-startX+offsetX, -startY+offsetY);
            c.drawPath(p, paint);
        }

        return b;

    }

    public static PathObject getPathFromAxis(JSONArray paths) throws Exception{
        PathObject obj = new PathObject();
        int minX = -1;
        int minY = -1;
        int maxX = -1;
        int maxY = -1;
        Path p = new Path();

       for(int i=0; i<paths.length(); i++){
           JSONArray points = paths.getJSONArray(i);
           obj.points.add(points);
           for(int j=0; j<points.length() ; j++) {
               JSONArray point = points.getJSONArray(j);
               int x = point.getInt(0);
               int y = point.getInt(1);
               if (j == 0) {
                   p.moveTo(x, y);
               } else {
                   p.lineTo(x, y);
               }

               minX = (minX == -1) ? x : Math.min(x, minX);
               maxX = (maxX == -1) ? x : Math.max(x, maxX);
               minY = (minY == -1) ? y : Math.min(y, minY);
               maxY = (maxY == -1) ? y : Math.max(y, maxY);
           }
           obj.paths.add(p);
           obj.minX = minX;
           obj.minY = minY;
           obj.maxX = maxX;
           obj.maxY = maxY;
       }
        return obj;
    }

}
