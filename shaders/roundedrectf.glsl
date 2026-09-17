#version 330 core

in vec2 frag_local_position;

uniform vec4 color;
uniform vec2 rect_size;
uniform float border_radius;

out vec4 fragColor;

float rounded_box(vec2 p, vec2 half_size, float radius)
{
    vec2 q = abs(p) - half_size + radius;

    return length(max(q, 0.0))
        + min(max(q.x, q.y), 0.0)
        - radius;
}

void main()
{
    vec2 p = frag_local_position * rect_size;
    p -= rect_size * 0.5;

    float distance = rounded_box(
        p,
        rect_size * 0.5,
        border_radius
    );

    float alpha = 1.0 - smoothstep(
        0.0,
        fwidth(distance),
        distance
    );

    fragColor = vec4(
        color.rgb,
        color.a * alpha
    );
}